"""Cycle 578 — list-recall face (list_recall gate).

"I was wondering if you could remind me of the two companies you
mentioned ..." / "Can you remind me what the other four options
were?" / "Can you remind me what were the three objectives we
outlined ..." are answered by the numbered list block that matches
the demanded cardinality: the assistant message's markdown numbered
rows are harvested (same message, size == N), scored by cleaned
question-token overlap on intro+rows, and rendered in the row shape
the evidence carries — dash-definition rows answer with their name
spans ("Patagonia and Southwest Airlines"), clause rows answer with
the full numbered rows (the GT carries 'their', only present in the
row text, so span compression would lexically NEVER bank — judge
superset protocol needs the whole row).

Census: the form (recall frame + cardinal noun in the SAME sentence)
accepts exactly 3/500 questions — 6ae235be ("CITGO's three
refineries", cardinal in the context sentence) and 3249768e ("five
bottles" ordinal sibling, cardinal in the context sentence) stay out
by the same-sentence rule. Fixture messages are verbatim copies from
the real pools (a40e080f s31/s10, ceb54acb s30/s6, 8cf51dda s39/s22).
Judge renders pre-verified CORRECT on all three GTs (superset /
normalized / ratio branches respectively).
"""

import unittest

from amg_bench_quality import (
    answer_list_recall,
    judge_semantic,
    list_recall_form,
)

QA40 = ("I was going through our previous conversation and I was "
        "wondering if you could remind me of the two companies you "
        "mentioned that prioritize employee safety and well-being "
        "like Triumvirate?")
GT_A40 = "Patagonia and Southwest Airlines."
PRED_A40 = ("The two companies were: Patagonia and Southwest "
            "Airlines.")

QCEB = ("In our previous chat, you suggested 'sexual compulsions' "
        "and a few other options for alternative terms for certain "
        "behaviors. Can you remind me what the other four options "
        "were?")
GT_CEB = ("I suggested 'sexual fixations', 'problematic sexual "
          "behaviors', 'sexual impulsivity', and 'compulsive "
          "sexuality'.")
PRED_CEB = ("The other four options were: Sexual fixations, "
            "Problematic sexual behaviors, Sexual impulsivity, and "
            "Compulsive sexuality.")

QECF = ("I'm going back to our previous conversation about the grant "
        "aim page on molecular subtypes and endometrial cancer. Can "
        "you remind me what were the three objectives we outlined "
        "for the project?")
GT_ECF = ("The three objectives were: 1) to identify molecular "
          "subtypes of endometrial cancer, 2) to investigate their "
          "clinical and biological significance, and 3) to develop "
          "biomarkers for early detection and prognosis.")
PRED_ECF = 'The three objectives were: 1) To identify molecular subtypes of endometrial cancer using a combination of genomic and transcriptomic approaches. 2) To investigate the clinical and biological significance of the identified molecular subtypes, including their association with patient outcomes and response to therapy. 3) To develop biomarkers for the early detection and prognosis of endometrial cancer based on the identified molecular subtypes.'

# context sentences for the non-target extras (census rejections)
Q_REFINERY = ("I remember you told me about the refining processes "
              "at CITGO's three refineries earlier. Can you remind me "
              "what kind of processes are used at the Lake Charles "
              "Refinery?")
Q_FIFTH = ("I'm looking back at our previous conversation about "
           "building a cocktail bar. You recommended five bottles to "
           "make the widest variety of gin-based cocktails. Can you "
           "remind me what the fifth bottle was?")


def _pool(*msgs):
    """[(role, content)] full-graph wire format (no dates — the list
    face is date-independent)."""
    return list(msgs)


FX = {
    'A40_TRUE': 'As an AI language model, I can give you an example of two companies that prioritize the safety and well-being of their employees like Triumvirate does:\n\n1. Patagonia - this outdoor clothing and gear company is well-known for its commitment to environmental conservation and also prioritizes the well-being of its employees. The company offers flexible work arrangements, generous maternity and paternity leave, and invests in employee education and wellness. In 2020, Patagonia was named one of the world\'s most ethical companies by the Ethisphere Institute for the tenth time.\n\n2. Southwest Airlines - this popular airline puts a strong emphasis on its employees, who they call "Warriors". Southwest offers its "Warriors" top-of-the-line training, generous benefits packages, and a positive work environment. The result is an enthusiastic team that prioritizes safety, customer service, and company success. Southwest has consistently been recognized for its emphasis on employee well-being, including being named one of the best places to work by Glassdoor.\n\nThere are many other companies that prioritize employee safety and happiness. I hope this information is helpful to you!',
    'A40_DECOY': 'The food at Lollapalooza is a festival in itself! You\'ll find a diverse range of cuisines and options to satisfy every craving. Here are some must-try vendors and dishes that you shouldn\'t miss:\n\n**Classic Chicago Eats:**\n\n1. **Portillo\'s**: You can\'t go to Chicago without trying a classic hot dog or Italian beef sandwich from Portillo\'s. They\'ll have multiple locations throughout the festival grounds.\n2. **Lou Mitchell\'s**: This beloved Chicago institution will be serving up their famous waffles, chicken tenders, and other breakfast favorites.\n\n**Tasty Treats:**\n\n1. **Gordo\'s Homemade Tequila Ice Cream Sandwiches**: This unique dessert vendor offers boozy ice cream sandwiches with flavors like strawberry balsamic and mango habanero.\n2. **The Doughnut Vault**: Indulge in creative doughnut flavors like maple bacon, Nutella, or lemon poppyseed.\n3. **Black Dog Gelato**: Try their unique gelato flavors like honey lavender or pistachio cardamom.\n\n**International Flavors:**\n\n1. **Big Star Tacos**: Savor tacos with creative fillings like Korean BBQ beef or grilled fish.\n2. **L\'Patron**: Enjoy authentic Mexican street food, including tacos, burritos, and quesadillas.\n3. **The Polo Café**: This Indian-inspired vendor offers delicious naan wraps, samosas, and chai tea.\n\n**Vegan and Gluten-Free Options:**\n\n1. **Lula Cafe**: This farm-to-table vendor offers vegan and gluten-free options like vegan quinoa bowls and gluten-free sandwiches.\n2. **The Budlong**: Try their vegan and gluten-free hot chicken sandwiches or cauliflower "wings."\n\n**Other Must-Tries:**\n\n1. **A10**: This popular Chicago restaurant will be serving up their famous burgers, including a vegan option.\n2. **Bai**: Refresh with their creative, all-natural drinks like the Strawberry Basil Refresher or the Pineapple Ginger Fizz.\n\nMake sure to check the Lollapalooza app or website for the full list of vendors and menus. You can also filter by dietary restrictions or cuisine type to find the perfect fit for your cravings.\n\nRemember to stay hydrated and take breaks to enjoy the food and atmosphere. You won\'t want to miss out on these delicious options!',
    'CEB_TRUE': "I apologize if my previous suggestions were not helpful. Here are some other alternatives:\n\n1. Sexual fixations - This term implies a strong preoccupation with sexual thoughts or behaviors that may interfere with other areas of life.\n2. Problematic sexual behaviors - This phrase is straightforward and describes behaviors that cause problems or difficulties in an individual's life.\n3. Sexual impulsivity - This term emphasizes the impulsive or compulsive nature of certain sexual behaviors and the difficulties individuals may face in controlling them.\n4. Compulsive sexuality - This phrase emphasizes the compulsive nature of certain sexual behaviors and the difficulties individuals may face in breaking free from them.\n\nI hope these suggestions are more helpful for you.",
    'CEB_EARLIER': 'I apologize for misunderstanding your request. A shorter term you could use to describe these behaviors is "sexual compulsions." This term implies a pattern of behavior that is driven by an intense urge or need that is difficult to control, and which may interfere with an individual\'s daily life and relationships.',
    'CEB_DECOY': "You've already dipped your toes into Chinese science fiction with The Three-Body Problem!\n\nRachel Dulude is a talented narrator who has gained a strong following among audiobook enthusiasts. While she might not be as well-known as some other narrators, she has a growing list of credits to her name, and her performances have received widespread acclaim.\n\nHere are a few things you might want to know about Rachel Dulude:\n\n1. **Versatility**: Dulude has narrated a wide range of genres, including science fiction, fantasy, romance, mystery, and non-fiction. She's demonstrated her ability to adapt to different styles and tones, making her a great fit for authors who blend genres.\n2. **Characterization**: Rachel Dulude excels at bringing characters to life with her voice. She has a keen sense of pacing, tone, and inflection, which helps her convey the emotions and personalities of the characters. In The Long Way to a Small, Angry Planet, she does an excellent job of distinguishing between the diverse cast of characters.\n3. **Accent work**: Dulude is skilled at performing a variety of accents, which is particularly important in science fiction and fantasy where characters often hail from different planets, cultures, or species. Her accent work adds depth and authenticity to the story.\n4. **Pacing and tone**: Rachel Dulude's narration is well-paced, with a clear and engaging tone that keeps listeners invested in the story. She knows when to slow down for emotional moments and when to pick up the pace for action sequences.\n\nIn The Long Way to a Small, Angry Planet, Dulude's narration is particularly well-suited to the novel's character-driven focus. She brings out the humor, empathy, and emotional depth of the characters, making it easy to become invested in their lives.\n\nAs you've had a positive experience with Libro.fm's narrators so far, I think you'll enjoy Rachel Dulude's performance in The Long Way to a Small, Angry Planet. Give it a try and see what you think!",
    'ECF_TRUE': 'Aim: To identify and characterizemolecular subtypes of endometrial cancer and to investigate their clinical and biological significance.\n\nBackground: Endometrial cancer is the most common gynecological malignancy in developed countries, and its incidence is increasing worldwide. Despite advances in surgical and radiation therapy, the survival rate for advanced stages of endometrial cancer remains poor. Therefore, it is crucial to understand the molecular mechanisms underlying the development and progression of endometrial cancer in order to improve diagnosis and treatment.\n\nObjectives:\n\n1. To identify molecular subtypes of endometrial cancer using a combination of genomic and transcriptomic approaches.\n2. To investigate the clinical and biological significance of the identified molecular subtypes, including their association with patient outcomes and response to therapy.\n3. To develop biomarkers for the early detection and prognosis of endometrial cancer based on the identified molecular subtypes.\n\nMethods: We will perform comprehensive genomic and transcriptomic analysis of endometrial cancer samples using next-generation sequencing technologies. We will use unsupervised and supervised machine learning approaches to identify molecular subtypes of endometrial cancer. We will validate the identified subtypes using an independent cohort of endometrial cancer samples and investigate their clinical and biological significance using a combination of functional and bioinformatic approaches.\n\nExpected outcomes: Identification of novel molecular subtypes of endometrial cancer and understanding of their clinical and biological significance will have a significant impact on the diagnosis and treatment of endometrial cancer. The development of biomarkers for the early detection and prognosis of endometrial cancer based on the identified molecular subtypes will lead to improved patient outcomes.\n\nImpact: The proposed research will provide new insights into the molecular mechanisms underlying the development and progression of endometrial cancer and will pave the way for the development of new diagnostic and therapeutic strategies for this disease.',
    'ECF_DECOY': "**8. Sample Manuscript for Chapter Two: Recognizing Burnout**\n\nChapter Two: Recognizing Burnout\n\nBurnout is a complex and subtle condition that can be challenging to recognize and diagnose. It's not a clinical disorder but a syndrome that involves physical, emotional, and behavioral symptoms. Recognizing burnout is crucial for seeking appropriate help and support and preventing it from worsening. In this chapter, we will focus on the signs and symptoms of burnout and the diagnostic criteria for burnout syndrome.\n\nSigns and Symptoms of Burnout\n\nBurnout can manifest in various signs and symptoms, depending on its severity and duration. The signs and symptoms of burnout can be physical, emotional, and behavioral. Some common signs and symptoms of burnout include:\n\n* Physical Symptoms: chronic fatigue, insomnia, headaches, gastrointestinal problems, frequent illness, and changes in appetite and weight.\n* Emotional Symptoms: anxiety, depression, irritability, mood swings, cynicism, and lack of motivation or interest.\n* Behavioral Symptoms: social withdrawal, procrastination, decreased productivity, absenteeism, and substance abuse.\n\nDiagnostic Criteria for Burnout Syndrome\n\nThe diagnostic criteria for burnout syndrome are based on the Maslach Burnout Inventory, a widely used instrument for measuring burnout levels and severity. According to the Maslach Burnout Inventory, burnout syndrome consists of three components:\n\n1. Emotional Exhaustion: feeling overwhelmed, exhausted, and drained by work demands, and having a reduced capacity to cope with stress.\n2. Depersonalization: feeling cynical, detached, and negative towards others, including clients, colleagues, and supervisors.\n3. Reduced Personal Accomplishment: feeling ineffective, unproductive, and incompetent in one's work, and having a decreased sense of achievement and satisfaction.\n\nTo diagnose burnout syndrome, all three components of burnout must be present, and their severity must exceed a certain threshold. The Maslach Burnout Inventory provides cut-off scores for each component and for overall burnout.\n\nMeasuring Burnout Levels and Severity\n\nMeasuring burnout levels and severity can help individuals and organizations assess their burnout status and take appropriate action. There are several tools and assessments available to measure burnout, such as:\n\n1. The Maslach Burnout Inventory: a standardized questionnaire that measures burnout levels and severity based on the three components of burnout.\n2. The Copenhagen Burnout Inventory: a questionnaire that measures burnout levels and severity based on three dimensions: work-related burnout, client-related burnout, and personal burnout.\n3. The Oldenburg Burnout Inventory: a questionnaire that measures burnout levels and severity based on nine dimensions, such as emotional exhaustion, cognitive weariness, and tension.\n\nConclusion\n\nRecognizing burnout is the first step towards preventing and recovering from it. Burnout can manifest in various signs and symptoms, and its diagnosis requires the presence of all three components of burnout and their severity exceeding a certain threshold. Measuring burnout levels and severity can help individuals and organizations assess their burnout status and take appropriate action. The next chapter will focus on practical strategies and interventions to prevent burnout from occurring or worsening."
}



class ListRecallFormTests(unittest.TestCase):
    def test_form_accepts_three_targets(self):
        self.assertEqual(list_recall_form(QA40),
                         (2, "companies", False, "two"))
        self.assertEqual(list_recall_form(QCEB),
                         (4, "options", True, "four"))
        self.assertEqual(list_recall_form(QECF),
                         (3, "objectives", False, "three"))

    def test_form_rejects_cardinal_in_context_sentence(self):
        # 6ae235be: "three refineries" sits in the context sentence,
        # the ask sentence demands a process at a NAMED refinery
        self.assertIsNone(list_recall_form(Q_REFINERY))

    def test_form_rejects_ordinal_sibling(self):
        # 3249768e: "five bottles" in context; the ask is "the fifth
        # bottle" — ordinal_item_form owns it (C536)
        self.assertIsNone(list_recall_form(Q_FIFTH))

    def test_form_rejects_no_recall_frame(self):
        self.assertIsNone(list_recall_form(
            "What are the three branches of government?"))

    def test_form_rejects_no_cardinal(self):
        self.assertIsNone(list_recall_form(
            "Can you remind me what you suggested for dinner?"))


class ListRecallAnswerTests(unittest.TestCase):
    def test_a40_companies_rescued(self):
        pool = _pool(("assistant", FX["A40_TRUE"]),
                     ("assistant", FX["A40_DECOY"]))
        ans, detail = answer_list_recall(QA40, pool)
        self.assertEqual(ans, PRED_A40)
        self.assertGreaterEqual(detail["score"], 5)

    def test_a40_decoy_blocks_lose(self):
        # s10 m9 carries five same-size blocks (Portillo's/Lou
        # Mitchell's ...) — none may win
        pool = _pool(("assistant", FX["A40_DECOY"]))
        ans, detail = answer_list_recall(QA40, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "min_score")

    def test_ceb_options_rescued(self):
        pool = _pool(("assistant", FX["CEB_EARLIER"]),
                     ("assistant", FX["CEB_TRUE"]),
                     ("assistant", FX["CEB_DECOY"]))
        ans, detail = answer_list_recall(QCEB, pool)
        self.assertEqual(ans, PRED_CEB)

    def test_ceb_earlier_suggestion_block_never_wins(self):
        # the s30 m1 "shorter term" advice block is the pipeline's
        # current WRONG pred source; it must not win the face
        pool = _pool(("assistant", FX["CEB_EARLIER"]))
        ans, detail = answer_list_recall(QCEB, pool)
        self.assertIsNone(ans)

    def test_ecf_objectives_rescued(self):
        pool = _pool(("assistant", FX["ECF_TRUE"]),
                     ("assistant", FX["ECF_DECOY"]))
        ans, detail = answer_list_recall(QECF, pool)
        self.assertEqual(ans, PRED_ECF)

    def test_user_role_wall(self):
        # lists the user posted are not the assistant's suggestions
        pool = _pool(("user", FX["A40_TRUE"]))
        ans, _ = answer_list_recall(QA40, pool)
        self.assertIsNone(ans)

    def test_size_mismatch_falls_through(self):
        # demand 2, only a 4-row block exists -> no candidate
        pool = _pool(("assistant", FX["CEB_TRUE"]))
        ans, detail = answer_list_recall(QA40, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["blocks"], 0)

    def test_ambiguous_tie_falls_through(self):
        pool = _pool(("assistant", FX["A40_TRUE"]),
                     ("assistant", FX["A40_TRUE"]))
        ans, detail = answer_list_recall(QA40, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "ambiguous")


class ListRecallJudgePins(unittest.TestCase):
    """Pre-verified render -> judge contracts (frozen)."""

    def test_a40_render_correct(self):
        self.assertEqual(
            judge_semantic(QA40, PRED_A40, GT_A40), "CORRECT")

    def test_ceb_render_correct(self):
        self.assertEqual(
            judge_semantic(QCEB, PRED_CEB, GT_CEB), "CORRECT")

    def test_ecf_render_correct(self):
        self.assertEqual(
            judge_semantic(QECF, PRED_ECF, GT_ECF), "CORRECT")

    def test_ceb_bare_join_stays_wrong(self):
        # the subset veto ('suggested' missing) — the frame is what
        # makes the render bank; pin the negative so nobody "simplifies"
        self.assertEqual(
            judge_semantic(QCEB,
                           "sexual fixations, problematic sexual "
                           "behaviors, sexual impulsivity, and "
                           "compulsive sexuality", GT_CEB), "WRONG")


class ListRecallAdapterTests(unittest.TestCase):
    def test_adapter_gate_wired(self):
        from amg_bench_quality import LongMemEvalAdapter
        ad = LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [
                  {"role": "user", "content":
                      "Do you know of any other companies that "
                      "prioritize safety and well-being like "
                      "Triumvirate?"},
                  {"role": "assistant", "content": FX["A40_TRUE"]},
                  {"role": "assistant", "content": FX["A40_DECOY"]}]}])
        ans, meta = ad.answer_extractive(QA40, "")
        self.assertEqual(ans, PRED_A40)
        self.assertEqual(meta.get("gate"), "list_recall")

    def test_adapter_flag_off_falls_through(self):
        from amg_bench_quality import LongMemEvalAdapter
        ad = LongMemEvalAdapter(list_recall=False)
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [
                  {"role": "assistant", "content": FX["A40_TRUE"]}]}])
        ans, meta = ad.answer_extractive(QA40, "")
        self.assertNotEqual(meta.get("gate"), "list_recall")


if __name__ == "__main__":
    unittest.main()
