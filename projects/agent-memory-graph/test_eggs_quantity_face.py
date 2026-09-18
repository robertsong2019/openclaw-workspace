# ════════ Cycle 586: recipe-ingredient-quantity face (eggs) ════════
# e8a79c70 census-first miniatures. Fixtures are VERBATIM dataset
# content (repr-injected by step3_gen_fixture.py): session_8 is the
# winning "classic French omelette" conversation (assistant recipe
# block carries the "-2-3 eggs" bullet — 9 chars, DROPPED by the
# 10-char _split_sentences floor, hence the bullet side-channel);
# session_14 is the "outstanding 3 egg omelette" decoy ("3 large
# eggs" bullet, zero french/classic mentions → topic-gated out).
import pytest

from amg_bench_quality import (LongMemEvalAdapter,
                               eggs_quantity_form,
                               answer_eggs_quantity)

QUESTION = 'I was going through our previous conversation about making a classic French omelette, and I wanted to confirm - how many eggs did you say we need for the recipe?'

S8 = [
        {"role": 'user', "content": 'What are the essential ingredients and steps to make a classic French omelette?'},
        {"role": 'assistant', "content": 'Ingredients:\n-2-3 eggs\n-A pinch of salt\n-1 tablespoon of unsalted butter\n-1 tablespoon of finely chopped herbs (optional)\n\nSteps:\n1. In a small mixing bowl, whisk the eggs with a pinch of salt until the mixture is well combined and the egg whites and yolks are fully incorporated.\n2. Heat a nonstick skillet over medium-high heat until it is hot enough to melt the butter without it sizzling or browning.\n3. Add one tablespoon of unsalted butter to the skillet, and swirl it around until it covers the entire surface of the skillet.\n4. When the butter has melted and is evenly distributed across the surface of the skillet, pour the egg mixture into the skillet, and use a fork or spatula to spread it evenly across the surface of the skillet.\n5. Let the mixture cook for about 30 seconds, or until the eggs begin to set.\n6. Gently lift one edge of the omelette with a spatula and fold it over the center of the omelette.\n7. Use the spatula to fold the opposite side over the center of the omelette.\n8. Tilt the skillet slightly to one side, and use the spatula to slide the omelette onto a plate.\n9. Garnish with chopped herbs, if desired.'},
        {"role": 'user', "content": 'That sounds easy enough! Do you have any tips for making the omelette fluffy and light?'},
        {"role": 'assistant', "content": "Yes, here are a few tips to make your French omelette light and fluffy:\n\n1. Whisk the eggs well: Make sure to whisk the eggs well until the mixture becomes frothy and the yolks and whites are fully combined.\n\n2. Use a nonstick skillet: A nonstick skillet will help prevent the omelette from sticking and tearing when you fold it. It also helps to cook the eggs evenly.\n\n3. Keep the heat medium-high: Don't cook your omelette over too high or too low heat. Overcooking can cause the omelette to become dry and rubbery. Cook the omelette over medium-high heat to make it fluffy and light.\n\n4. Don't overfill the omelette: Keep the omelette filling light to prevent it from becoming too heavy.\n\n5. Fold the omelette gently: To get the light and fluffy texture, you want to fold the omelette gently, using a spatula. Don't press down too hard, or you could flatten the egg mixture and make it dense.\n\n6. Serve immediately: Serve the omelette immediately after folding to prevent it from getting cold and potentially limp. Enjoy your fluffy and light French omelette!"},
        {"role": 'user', "content": "I can't wait to try making a classic French omelette now. Do you have any recommendations for fillings?"},
        {"role": 'assistant', "content": 'Yes, here are a few tasty fillings you can try for your classic French omelette:\n\n1. Cheese: Add grated cheese such as Swiss, cheddar, or Gruyere to the omelette before folding. 2. Ham: Cooked ham, diced and sautéed in butter, is a classic filling for French omelettes. 3. Mushrooms: Sautéed mushrooms add a delicious earthy flavor to omelettes. 4. Spinach: Cooked spinach, along with sautéed onions and garlic, make a tasty filling for omelettes. 5. Tomatoes: Diced, cooked tomatoes can add a nice juicy burst of flavor to your omelette. 6. Herbs: Add fresh or dried herbs such as parsley, thyme, or chives to the egg mixture for extra flavor and aroma. Remember not to overfill your omelette – just a few tablespoons of filling will be enough. Enjoy your delicious omelette!'},
        {"role": 'user', "content": 'Yum, all of those fillings sound amazing! Do you have a personal favorite?'},
        {"role": 'assistant', "content": "As an AI language model, I don't have personal preferences. However, here are some great combinations that people usually prefer:\n\n- Ham and cheese: This classic filling is always a winner, and you can use any type of cheese you like.\n\n- Mushroom and cheese: Sautéed mushrooms and grated cheese make a delicious and savory filling.\n\n- Spinach and feta: Cooked spinach and crumbled feta cheese make a healthy and flavorful filling.\n\n- Tomato and basil: Diced tomatoes and chopped fresh basil add a burst of summer flavor to omelettes.\n\n- Smoked salmon and dill: For a more elegant omelette, you can use smoked salmon and dill as a filling.\n\nRemember, you can always experiment with different fillings and see what works best for you. Have fun cooking!"},
]

S14 = [
        {"role": 'user', "content": 'Can you provide a more comprehensive answer'},
        {"role": 'assistant', "content": "Sure, here is a more comprehensive answer with additional details:\n\n1. Determine the Design Point: The first step in designing a centrifugal impeller is to determine the design point, which is the operating condition at which the impeller will operate. The design point is typically defined by the desired flow rate (Q), pressure rise (ΔP), and rotational speed (N). In this case, the design point requires a specific speed (Ns) of 1000, which is a dimensionless parameter that relates the impeller's geometry and rotational speed to its performance.\n2. Determine the Geometric Parameters: Once the design point is known, the next step is to determine the geometric parameters of the impeller. These include the inlet diameter (D1), outlet diameter (D2), blade height (h), blade angle (β), and other parameters that may be required depending on the impeller design. The geometric parameters are typically determined based on empirical formulas, charts, or CFD analysis. The selection of geometric parameters depends on the design requirements and the operating conditions.\n3. Design the Blade Shape: The blade shape is a critical component of the impeller design, as it directly affects the fluid flow and the impeller's performance. The blade shape should be aerodynamically efficient, and should provide the desired flow rate and pressure rise. The blade shape is typically designed using CAD software and CFD analysis to optimize the shape for the design requirements.\n4. Determine the Number of Blades: The number of blades is another critical design parameter that affects the impeller's efficiency and stability. A higher number of blades typically result in higher pressure rise but lower flow rates, while fewer blades result in higher flow rates but lower pressure rise. The optimal number of blades depends on the impeller's design requirements and operating conditions, and may be determined through empirical formulas or CFD analysis.\n5. Perform CFD Analysis: Once the blade shape and number of blades have been determined, perform CFD analysis to evaluate the impeller's performance. CFD analysis provides a detailed understanding of the fluid flow and pressure distribution within the impeller, which can be used to optimize the design for efficiency and stability. CFD analysis may be performed using commercial software or custom-designed simulation tools.\n6. Prototype and Test: Finally, prototype the impeller and perform physical testing to validate the design and ensure it meets the desired performance criteria. Physical testing provides a more accurate representation of the impeller's performance under actual operating conditions, and can be used to fine-tune the design for optimal performance.\n\nIn addition to the above steps, there are many other considerations and design factors that may need to be taken into account when designing a centrifugal impeller, including material selection, manufacturing considerations, and noise reduction techniques. The design process for a centrifugal impeller is complex and requires expertise in fluid dynamics, CAD design, CFD analysis, and manufacturing."},
        {"role": 'user', "content": 'Give me a process and ingredients for an outstanding 3 egg omelette'},
        {"role": 'assistant', "content": "Sure, here's a process and ingredients for making an outstanding 3 egg omelette:\n\nIngredients:\n\n* 3 large eggs\n* 1 tablespoon of butter\n* Salt and pepper to taste\n* 2-3 tablespoons of shredded cheese (optional)\n* Fillings of your choice (e.g. chopped vegetables, ham, bacon, mushrooms, etc.)\n\nProcess:\n\n1. Crack the eggs into a bowl and whisk them together with a fork or whisk until the whites and yolks are completely blended. Add a pinch of salt and pepper to taste.\n2. Heat a non-stick skillet over medium-high heat and add the butter. Once the butter is melted and begins to foam, tilt the pan to make sure the butter covers the entire surface.\n3. Pour the egg mixture into the skillet and let it cook for about 10-15 seconds, until the edges begin to set.\n4. Use a spatula to gently lift and fold the edges of the omelette towards the center, allowing the uncooked egg to flow to the edges and cook. Repeat this process a few times until the top surface of the omelette is still slightly runny but the bottom is fully set.\n5. Add the fillings of your choice to one half of the omelette, and sprinkle with shredded cheese (if using).\n6. Use the spatula to gently fold the other half of the omelette over the fillings to create a half-moon shape.\n7. Let the omelette cook for another 1-2 minutes, until the cheese is melted and the filling is heated through.\n8. Use the spatula to carefully slide the omelette onto a plate and serve hot.\n\nTips:\n\n* Use a non-stick skillet to prevent the omelette from sticking and to make it easier to flip and fold.\n* Don't overfill the omelette with fillings, as this can make it difficult to fold and can result in a messy omelette.\n* Use high-quality ingredients, such as farm-fresh eggs and fresh vegetables, for the best flavor.\n* Experiment with different fillings and seasonings to create your own unique omelette recipes."},
        {"role": 'user', "content": 'Is there a way to print out out share your your responses without printing multiple pages'},
        {"role": 'assistant', "content": 'Yes, there are a few ways to print or share responses without printing multiple pages:\n\n1. Copy and paste the text into a document or email: Simply highlight the text of the response, right-click and select "Copy", then open a document or email and right-click and select "Paste" to insert the text. You can then print or share the document or email as needed.\n2. Use a "Print to PDF" feature: Many modern web browsers have a "Print to PDF" feature that allows you to save a webpage or document as a PDF file. Simply open the page with the response you want to save, click "Print" and select "Save as PDF" as the destination. You can then save or share the PDF file as needed.\n3. Use a web clipping tool: There are various web clipping tools available, such as Evernote or OneNote, that allow you to clip and save webpages or specific sections of a webpage. Simply install the tool, clip the section of the response you want to save, and then save or share the clip as needed.\n\nI hope these options are helpful!'},
        {"role": 'user', "content": 'Give me the ingredients and recipe for an outstanding spaghetti bolognese'},
        {"role": 'assistant', "content": "Sure, here's a recipe for an outstanding spaghetti bolognese:\n\nIngredients:\n\n* 1 lb ground beef\n* 1 onion, finely chopped\n* 2 garlic cloves, minced\n* 2 carrots, finely chopped\n* 2 celery stalks, finely chopped\n* 1 can (28 oz) crushed tomatoes\n* 1/2 cup red wine (optional)\n* 1/2 cup beef or chicken broth\n* 1 tsp dried oregano\n* 1 tsp dried basil\n* 1/2 tsp dried thyme\n* Salt and pepper to taste\n* 1 lb spaghetti\n* Grated Parmesan cheese for serving\n\nInstructions:\n\n1. In a large pot or Dutch oven, heat a tablespoon of oil over medium-high heat. Add the ground beef and cook until browned, breaking up any clumps with a wooden spoon. Transfer the beef to a plate and set aside.\n2. In the same pot, add the onion, garlic, carrots, and celery. Cook, stirring occasionally, until the vegetables are softened, about 5-7 minutes.\n3. Add the beef back to the pot and stir to combine with the vegetables.\n4. Pour in the crushed tomatoes, red wine (if using), and beef or chicken broth. Stir in the oregano, basil, thyme, salt, and pepper.\n5. Bring the mixture to a simmer, reduce the heat to low, and let it cook, partially covered, for at least 30 minutes, stirring occasionally. If the sauce is too thick, add more broth or water as needed.\n6. While the sauce is simmering, cook the spaghetti according to package instructions until al dente. Drain the spaghetti and reserve 1/2 cup of the pasta water.\n7. Add the cooked spaghetti to the pot with the sauce and toss to combine, adding reserved pasta water as needed to thin out the sauce.\n8. Serve hot with grated Parmesan cheese on top.\n\nTips:\n\n* If you want a thicker sauce, you can add a tablespoon of tomato paste or let the sauce simmer for longer.\n* You can also add other vegetables, such as mushrooms or bell peppers, to the sauce if desired.\n* For a vegetarian version, you can substitute the ground beef with chopped mushrooms or cooked lentils."},
        {"role": 'user', "content": 'Please provide these instructions using an instant pot'},
        {"role": 'assistant', "content": 'Sure, here\'s how to make spaghetti bolognese using an Instant Pot:\n\nIngredients:\n\n* 1 lb ground beef\n* 1 onion, finely chopped\n* 2 garlic cloves, minced\n* 2 carrots, finely chopped\n* 2 celery stalks, finely chopped\n* 1 can (28 oz) crushed tomatoes\n* 1/2 cup red wine (optional)\n* 1/2 cup beef or chicken broth\n* 1 tsp dried oregano\n* 1 tsp dried basil\n* 1/2 tsp dried thyme\n* Salt and pepper to taste\n* 1 lb spaghetti\n* Grated Parmesan cheese for serving\n\nInstructions:\n\n1. Set the Instant Pot to "Sauté" mode and add a tablespoon of oil. Add the ground beef and cook until browned, breaking up any clumps with a wooden spoon. Transfer the beef to a plate and set aside.\n2. In the same pot, add the onion, garlic, carrots, and celery. Cook, stirring occasionally, until the vegetables are softened, about 5-7 minutes.\n3. Add the beef back to the pot and stir to combine with the vegetables.\n4. Pour in the crushed tomatoes, red wine (if using), and beef or chicken broth. Stir in the oregano, basil, thyme, salt, and pepper.\n5. Close the Instant Pot lid and set it to "Manual" mode for 10 minutes at high pressure.\n6. Once the cooking time is complete, let the pressure release naturally for 10 minutes, then use the quick release method to release any remaining pressure.\n7. While the sauce is cooking, cook the spaghetti according to package instructions until al dente. Drain the spaghetti and reserve 1/2 cup of the pasta water.\n8. Once the pressure has released, open the Instant Pot lid and stir the sauce. If the sauce is too thin, you can set the Instant Pot to "Sauté" mode and let it simmer for a few minutes to thicken.\n9. Add the cooked spaghetti to the pot with the sauce and toss to combine, adding reserved pasta water as needed to thin out the sauce.\n10. Serve hot with grated Parmesan cheese on top.\n\nTips:\n\n* If you want a thicker sauce, you can add a tablespoon of tomato paste or let the sauce simmer for longer in step 8.\n* You can also add other vegetables, such as mushrooms or bell peppers, to the sauce if desired.\n* For a vegetarian version, you can substitute the ground beef with chopped mushrooms or cooked lentils.'},
]


def _ingest(*sessions, **kw):
    ad = LongMemEvalAdapter(**kw)
    ad.ingest_sessions([{"session_id": f"session_{i+1}",
                          "messages": list(s)}
                       for i, s in enumerate(sessions)])
    return ad


# ── form ──

def test_form_accept():
    assert eggs_quantity_form(QUESTION) == "classic French omelette"


def test_form_reject_no_recall_frame():
    # stocked-up phrasing: no "did you say" recall demand
    q = "How many eggs do we currently have stocked up in our refrigerator?"
    assert eggs_quantity_form(q) is None


def test_form_reject_no_egg_demand():
    q = ("I remember our conversation about making a classic French "
         "omelette - what pan did you say we need?")
    assert eggs_quantity_form(q) is None


def test_form_reject_no_topic_np():
    # egg demand + recall frame but NO "conversation about making a X"
    q = "How many eggs did you say we need for the recipe?"
    assert eggs_quantity_form(q) is None


# ── answer face ──

def test_rescue_winner_session():
    nodes = _ingest(S8)._nodes
    ans, detail = answer_eggs_quantity(QUESTION, nodes)
    assert ans == "2-3 eggs"
    assert detail["form"] == "eggs_quantity"
    assert detail["renders"] == ["2-3 eggs"]


def test_decoy_session_gated_out():
    # decoy present in the same graph: topic gate must still pick
    # session_8 (zero french/classic in session_14)
    nodes = _ingest(S8, S14)._nodes
    ans, detail = answer_eggs_quantity(QUESTION, nodes)
    assert ans == "2-3 eggs"
    assert detail["renders"] == ["2-3 eggs"]


def test_decoy_only_falls_through():
    # WITHOUT the topic-bound session the face must stay silent —
    # "3 large eggs" must never render
    nodes = _ingest(S14)._nodes
    ans, detail = answer_eggs_quantity(QUESTION, nodes)
    assert ans is None
    assert detail["reason"] == "no_match"


def test_ambiguous_falls_through():
    # two topic-bound sessions with disagreeing quantities
    mutated = [dict(m) for m in S14]
    mutated[2] = dict(mutated[2])
    mutated[2]["content"] = (
        "Let's revisit our conversation about making a classic French "
        "omelette, give me a process and ingredients")
    nodes = _ingest(S8, mutated)._nodes
    ans, detail = answer_eggs_quantity(QUESTION, nodes)
    assert ans is None
    assert detail["reason"] == "ambiguous"
    assert sorted(detail["renders"]) == ["2-3 eggs", "3 large eggs"]


def test_user_recipe_bullet_not_claimed():
    # "did you say" = assistant-role wall: a USER-carried egg bullet
    # in the topic-bound session must not render
    user_recipe = [dict(m) for m in S8]
    user_recipe[0] = dict(user_recipe[0])
    user_recipe[0]["content"] = (
        "What are the essential ingredients and steps to make a "
        "classic French omelette? I think it was -4-5 eggs?")
    nodes = _ingest(user_recipe)._nodes
    ans, detail = answer_eggs_quantity(QUESTION, nodes)
    assert ans == "2-3 eggs"   # assistant block still the only render


def test_no_egg_bullet_falls_through():
    topic_only = [dict(m) for m in S8]
    topic_only[1] = dict(topic_only[1])
    topic_only[1]["content"] = topic_only[1]["content"].replace(
        "-2-3 eggs\n", "-free-range eggs if you like\n")
    # no digit quantity anywhere in the bullet → not a quantity answer
    nodes = _ingest(topic_only)._nodes
    ans, detail = answer_eggs_quantity(QUESTION, nodes)
    assert ans is None


# ── adapter wiring ──

def test_adapter_gate_and_pred():
    ad = _ingest(S8, S14)
    ans, meta = ad.answer_extractive(QUESTION, "")
    assert meta.get("gate") == "eggs_quantity"
    assert ans == "2-3 eggs"


def test_adapter_flag_off_keeps_old_path():
    ad = _ingest(S8, S14, eggs_quantity_recall=False)
    ans, meta = ad.answer_extractive(QUESTION, "")
    assert meta.get("gate") != "eggs_quantity"
