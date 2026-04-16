import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import type { Agent, TrustRelation, GraphNode, GraphLink } from '../types';

interface NetworkGraphProps {
  agents: Agent[];
  relations: TrustRelation[];
  onNodeClick?: (agentId: string) => void;
  onNodeHover?: (agentId: string | null) => void;
}

const behaviorColors: Record<string, string> = {
  cooperative: '#3fb950',
  neutral: '#d29922',
  malicious: '#f85149',
  adversarial: '#bc8cff',
};

export const NetworkGraph: React.FC<NetworkGraphProps> = ({
  agents,
  relations,
  onNodeClick,
  onNodeHover,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const updateDimensions = () => {
      const { width, height } = container.getBoundingClientRect();
      setDimensions({ width, height });
    };

    updateDimensions();
    const resizeObserver = new ResizeObserver(updateDimensions);
    resizeObserver.observe(container);

    return () => resizeObserver.disconnect();
  }, []);

  useEffect(() => {
    if (!svgRef.current || dimensions.width === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const nodeMap = new Map<string, GraphNode>();
    const nodes: GraphNode[] = agents.map(agent => ({
      id: agent.id,
      name: agent.name,
      behavior: agent.behavior,
      trustScore: agent.trustScore,
      interactions: agent.interactions,
      successRate: agent.successRate,
      radius: 10 + agent.trustScore * 25,
    }));

    nodes.forEach(node => nodeMap.set(node.id, node));

    const links: GraphLink[] = relations
      .filter(r => nodeMap.has(r.from) && nodeMap.has(r.to))
      .map(r => ({
        source: r.from,
        target: r.to,
        weight: r.weight,
      }));

    // Create arrow marker
    const defs = svg.append('defs');
    defs
      .append('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 20)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('fill', '#30363d')
      .attr('d', 'M0,-5L10,0L0,5');

    // Create glow filter
    const filter = defs.append('filter').attr('id', 'glow');
    filter.append('feGaussianBlur').attr('stdDeviation', '3').attr('result', 'blur');
    filter
      .append('feMerge')
      .selectAll('feMergeNode')
      .data(['blur', 'SourceGraphic'])
      .join('feMergeNode')
      .attr('in', (d: any) => d);

    const g = svg.append('g');

    // Zoom behavior
    const zoom = d3
      .zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.3, 4])
      .on('zoom', (event) => g.attr('transform', event.transform));
    svg.call(zoom);

    // Links
    const link = g
      .append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', '#30363d')
      .attr('stroke-width', (d) => Math.max(0.5, (d.weight as number) * 3))
      .attr('stroke-opacity', (d) => 0.3 + (d.weight as number) * 0.5)
      .attr('marker-end', 'url(#arrow)');

    // Nodes
    const node = g
      .append('g')
      .selectAll<SVGGElement, GraphNode>('g')
      .data(nodes)
      .join('g')
      .call(
        d3
          .drag<SVGGElement, GraphNode>()
          .on('start', dragStarted)
          .on('drag', dragged)
          .on('end', dragEnded)
      );

    // Node circles
    node
      .append('circle')
      .attr('r', (d) => d.radius)
      .attr('fill', (d) => behaviorColors[d.behavior] || '#8b949e')
      .attr('fill-opacity', 0.85)
      .attr('stroke', (d) => d3.color(behaviorColors[d.behavior])?.brighter(0.5).toString() || '#8b949e')
      .attr('stroke-width', 2)
      .style('filter', 'url(#glow)')
      .on('click', (event, d) => {
        event.stopPropagation();
        onNodeClick?.(d.id);
      })
      .on('mouseover', (_event, d) => {
        onNodeHover?.(d.id);

        // Highlight connected links
        link
          .attr('stroke', (l) => {
            const sourceId = typeof l.source === 'string' ? l.source : (l.source as GraphNode).id;
            const targetId = typeof l.target === 'string' ? l.target : (l.target as GraphNode).id;
            return sourceId === d.id || targetId === d.id ? behaviorColors[d.behavior] : '#30363d';
          })
          .attr('stroke-opacity', (l) => {
            const sourceId = typeof l.source === 'string' ? l.source : (l.source as GraphNode).id;
            const targetId = typeof l.target === 'string' ? l.target : (l.target as GraphNode).id;
            return sourceId === d.id || targetId === d.id ? 0.8 : 0.1;
          })
          .attr('stroke-width', (l) => {
            const sourceId = typeof l.source === 'string' ? l.source : (l.source as GraphNode).id;
            const targetId = typeof l.target === 'string' ? l.target : (l.target as GraphNode).id;
            return sourceId === d.id || targetId === d.id ? Math.max(1, (l.weight as number) * 5) : Math.max(0.5, (l.weight as number) * 3);
          });
      })
      .on('mouseout', (_event: React.MouseEvent) => {
        onNodeHover?.(null);
        link
          .attr('stroke', '#30363d')
          .attr('stroke-opacity', (d) => 0.3 + (d.weight as number) * 0.5)
          .attr('stroke-width', (d) => Math.max(0.5, (d.weight as number) * 3));
      });

    // Node labels
    node
      .append('text')
      .attr('dy', (d) => d.radius + 14)
      .attr('text-anchor', 'middle')
      .attr('fill', '#8b949e')
      .attr('font-size', '10px')
      .text((d) => d.name);

    // Force simulation
    const simulation = d3
      .forceSimulation(nodes)
      .force(
        'link',
        d3
          .forceLink<GraphNode, GraphLink>(links)
          .id((d: any) => d.id)
          .distance(80)
          .strength((d) => (d.weight as number) * 0.3)
      )
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(dimensions.width / 2, dimensions.height / 2))
      .force('collision', d3.forceCollide().radius((d: any) => (d as GraphNode).radius + 5));

    simulation.on('tick', () => {
      link
        .attr('x1', (d) => (d.source as GraphNode).x!)
        .attr('y1', (d) => (d.source as GraphNode).y!)
        .attr('x2', (d) => (d.target as GraphNode).x!)
        .attr('y2', (d) => (d.target as GraphNode).y!);

      node.attr('transform', (d) => `translate(${d.x},${d.y})`);
    });

    function dragStarted(event: d3.D3DragEvent<SVGGElement, GraphNode, GraphNode>, d: GraphNode) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: d3.D3DragEvent<SVGGElement, GraphNode, GraphNode>, d: GraphNode) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragEnded(event: d3.D3DragEvent<SVGGElement, GraphNode, GraphNode>, d: GraphNode) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [agents, relations, dimensions, onNodeClick, onNodeHover]);

  return (
    <div ref={containerRef} className="w-full h-full">
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        className="w-full h-full"
      />
    </div>
  );
};
