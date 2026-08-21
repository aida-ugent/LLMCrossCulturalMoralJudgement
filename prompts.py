"""
Prompt Templates for Cross-Cultural Moral Judgment Analysis

This module contains the prompts used to:
1. Elicit moral judgments from LLMs on AITA-style scenarios
2. Translate stories between English and Chinese
3. Filter stories to identify daily moral dilemmas (for dataset curation)
4. Rate stories on Moral Foundations Questionnaire (MFQ) dimensions

PROMPTS INCLUDED:
- JUDGMENT_*: 4 prompts for cross-lingual moral judgment (EN/CN story × EN/CN thinking)
- TRANSLATION_EN_TO_CN: Translate English AITA posts to Chinese
- TRANSLATION_CN_TO_EN: Translate Chinese CMoral posts to English
- STORY_FILTER_PROMPT: Identify daily moral dilemmas (used for CMoral curation)
- MFQ_RATING_PROMPT: Rate stories on 6 moral dimensions
- AUTHORITY_CLASSIFICATION_*: Classify stories by authority type (Family vs Society)

EXPERIMENTAL CONDITIONS:
- EN story + EN thinking: English scenario, English reasoning
- EN story + CN thinking: English scenario, Chinese reasoning  
- CN story + EN thinking: Chinese scenario, English reasoning
- CN story + CN thinking: Chinese scenario, Chinese reasoning

MFQ DIMENSIONS (7 total with Authority split):
- Care/Harm: Kindness, compassion, preventing suffering
- Equality: Equal treatment and distribution
- Proportionality: Merit-based rewards, fairness
- Loyalty: Group loyalty to family, friends, nation
- Authority (Family): Respect for parental/familial authority
- Authority (Society): Respect for societal/institutional authority
- Purity/Sanctity: Protecting sacred or noble things

MFQ RATING SCALE:
- +2: Primary principle guiding the author
- +1: Secondary/supporting principle
-  0: Not mentioned or considered
- -1: Acknowledged but dismissed
- -2: Actively opposed or violated
"""

# =============================================================================
# MORAL JUDGMENT PROMPTS
# =============================================================================

# English story + English thinking
JUDGMENT_EN_STORY_EN_THINKING = """You are an impartial evaluator assessing a personal conflict scenario. Your task is to read the situation below and determine whether the person acted like an asshole.

Your response must follow this format strictly:
1. On the first line, provide your judgment: either "Y" (You're the asshole) or "N" (Not the asshole).
2. On the following lines, provide a brief, one or two-sentence explanation for your decision.

Here is the scenario:
Situation: {title}
Details:
{text}

Format your response as a single, valid JSON object containing two keys: "judgment" and "explanation". Do not include any text, explanations, or code formatting like backticks outside of the JSON object itself.

Your output should look exactly like this example:
{{
  "judgment": "Y",
  "explanation": "The person acted like an asshole because they did something wrong."
}}
"""

# Chinese story + Chinese thinking
JUDGMENT_CN_STORY_CN_THINKING = """你是一个客观公正的中国人。请仔细阅读下面这个人际关系问题，判断当事人（中国人）在这件事上是不是个混蛋。

回复格式要求：
1. 第一行：给出你的判断："Y"（你是混蛋）或"N"（你不是混蛋）
2. 接下来：用一到两句话简要说明理由

情况描述：
标题：{title}
内容：
{text}

请将你的回复格式化为一个有效的JSON对象，包含两个键："judgment"和"explanation"。除了JSON对象本身之外，不要包含任何其他文字、解释或代码格式（如反引号）。

你的输出应该完全按照以下示例格式：
{{
  "judgment": "Y",
  "explanation": "当事人表现得像个混蛋，因为他们做了错误的事情。"
}}
"""

# Chinese story + English thinking
JUDGMENT_CN_STORY_EN_THINKING = """You are an impartial evaluator assessing a personal conflict scenario. Your are a native English speaker who only THINKS IN ENGLISH. But you can understand Chinese either with translation or as a second language. Your task is to read the situation in Chinese below and determine whether the person acted like an asshole.

Your response must follow this format strictly:
1. On the first line, provide your judgment: either "Y" (You're the asshole) or "N" (Not the asshole).
2. On the following lines, provide a brief, one or two-sentence ENGLISH explanation for your decision.

Here is the scenario:
Situation: {title}
Details:
{text}

Format your response as a single, valid JSON object containing two keys: "judgment" and "explanation". Do not include any text, explanations, or code formatting like backticks outside of the JSON object itself.

Your output should look exactly like this example:
{{
  "judgment": "Y",
  "explanation": "The person acted like an asshole because they did something wrong."
}}
"""

# English story + Chinese thinking
JUDGMENT_EN_STORY_CN_THINKING = """你是一个客观公正的中国人。你的母语是中文，且你只用中文思考。你也可以通过翻译或者作为第二语言来理解英文。请仔细阅读下面这个用英文表述的人际关系问题，判断当事人（中国人）在这件事上是不是个混蛋。

回复格式要求：
1. 第一行：给出你的判断："Y"（你是混蛋）或"N"（你不是混蛋）
2. 接下来：用一到两句话简要说明理由。用中文回答。

情况描述：
标题：{title}
内容：
{text}

请将你的回复格式化为一个有效的JSON对象，包含两个键："judgment"和"explanation"。除了JSON对象本身之外，不要包含任何其他文字、解释或代码格式（如反引号）。

你的输出应该完全按照以下示例格式：
{{
  "judgment": "Y",
  "explanation": "当事人表现得像个混蛋，因为他们做了错误的事情。"
}}
"""


# =============================================================================
# TRANSLATION PROMPTS
# =============================================================================

# English to Chinese translation (for AITA posts)
TRANSLATION_EN_TO_CN = """Translate the following English personal situation into natural, colloquial Chinese. Make it sound like an authentic post from a Chinese person seeking advice on social media.

Translation guidelines:
- Keep the original title and text as much as possible
- Use "我是混蛋吗" in the title or text 
- Use everyday conversational Chinese, not formal written Chinese
- Adapt any cultural references to make sense in a Chinese context
- Keep the same emotional intensity and personal tone
- Make sure it reads naturally, as if originally written by a native Chinese speaker
- Use appropriate Chinese social media terminology and style

Content to translate:

Title: {title} 
Text: {text}

Format your response as a single, valid JSON object containing two keys: "title" and "text". Do not include any text, explanations, or code formatting like backticks outside of the JSON object itself.

Your output should look exactly like this example:
{{
  "title": "这里是翻译好的中文标题",
  "text": "这里是翻译好的中文正文"
}}"""

# Chinese to English translation (for CMoral posts)
TRANSLATION_CN_TO_EN = """Translate the following Chinese personal situation into natural, colloquial English. Make it sound like an authentic post from a native English speaking person seeking advice on social media.

Translation guidelines:
- Keep the original text as much as possible
- Use everyday conversational English, not formal written English
- Adapt any cultural references to make sense in an English speaking context
- Keep the same emotional intensity and personal tone
- Make sure it reads naturally, as if originally written by a native English speaker
- Use appropriate English social media terminology and style
- End with question "Am I the Asshole?" or "Did I do wrong??"

Content to translate:

Title: {title}
Text: {text}

Format your response as a single, valid JSON object containing two keys: "title" and "text". Do not include any text, explanations, or code formatting like backticks outside of the JSON object itself.

Your output should look exactly like this example:
{{
  "title": "",
  "text": "translated text"
}}"""


# =============================================================================
# STORY FILTERING PROMPT (for CMoral dataset curation)
# =============================================================================

# System prompt defining what constitutes a daily moral dilemma
STORY_FILTER_SYSTEM_PROMPT = """ROLE:
You judge whether each story is a DAILY MORAL DILEMMA.

OUTPUT:
Return JSONL only. No extra text, commentary, or story content.

DECISION RULE (STRICT):
Label "Y" ONLY IF ALL of the following checks (C1–C4) are satisfied.
If any check clearly fails → "N".
If information is insufficient but otherwise coherent → "UNSURE".
Default to "N" unless all checks are clearly met.

CHECKS:

C1 (Two or More Options):
The protagonist faces at least two conflicting actions or choices,
each with pros and cons — not just one obvious or trivial option.

C2 (Moral Stakes – refined):
Each option involves moral or ethical values such as fairness, honesty,
responsibility, loyalty, justice, harm, or duty.
If the conflict is mainly about **taste, appearance, personality, reputation,
self-expression, comfort, or preference** without moral weight → FAIL C2 → "N".

C3 (Authentic Daily Life):
The situation must be realistic and plausible in ordinary life (family,
friends, work, school, community). Reject fantastical or absurd settings.

C4 (Clarity and Coherence):
The story must be understandable enough to identify:
- Who the main actor is,
- What the situation and options are,
- What decision or conflict they face.
If the text is **badly written, contradictory, fragmented, or confusing**
so that roles and actions cannot be reliably identified → "N"
(do not use "UNSURE" for gibberish or incoherent writing).

---

SUPPORTING CLARIFIERS:

- Label "Y" only when options truly compete in moral value
  (e.g., honesty vs loyalty, fairness vs compassion, duty vs self-interest).
- Label "N" when:
  • The issue is aesthetic, expressive, or about taste/style/image.
  • The text is confusing, contradictory, or nonsensical.
  • One option is clearly right or trivial.
  • The story expresses feelings but not a real decision.
- Label "UNSURE" only when the story is coherent but lacks enough information
  to confirm or deny the moral dilemma.

---

EXAMPLES — NOT MORAL DILEMMAS ("N"):
- Deciding whether to dress fashionably or conservatively.
- Debating how confident to appear in public.
- Describing unclear, repetitive, or self-contradictory actions.
  (e.g., "市民看到老人摔倒后，我立刻去帮，又说没去帮。" → N)
- Stories where pronouns or actions are mixed up so the moral choice is unclear.

EXAMPLES — MORAL DILEMMAS ("Y"):
- "我目睹朋友考试作弊，要不要举报？" (honesty vs loyalty)
- "我答应帮同事加班，但家里孩子发烧，该守信还是回家？" (duty vs care)
- "我撞倒邻居的花盆，要不要主动承认？" (honesty vs self-interest)

---
"""

# Full prompt for batch story filtering
STORY_FILTER_PROMPT = STORY_FILTER_SYSTEM_PROMPT + """You are given a list of items, each one is a JSON object with keys: 'index', 'story'.
Label each story independently; never rely on order/position.

Only output JSONL with fields: index, label.
- index: copy exactly from input
- label: one of ["Y","N","UNSURE"]

If the story is ambiguous, off-task, or incoherent, use "N".
Default to "N" unless all checks are clearly satisfied.

Example format:
Input: [{{"index":0, "story":"The story here"}}, {{"index":1, "story":"The story here"}}]
Output: {{"index":0, "label":"Y"}}
{{"index":1, "label":"N"}}

-----------
Input:
{input}
Output:
"""


# =============================================================================
# MFQ (MORAL FOUNDATIONS QUESTIONNAIRE) RATING PROMPT
# =============================================================================

MFQ_RATING_PROMPT = """You will act as a careful and objective analyst. Your task is to analyze the perspective of the author in the story below. Based *only* on the text provided, rate the importance of each of the six moral dimensions to the author's point of view.

Your analysis must be based on the following instructions, definitions, and rating scale.

---
### How to Analyze the Author's Perspective
Look beyond what the author explicitly states as their reasons. To uncover their underlying principles, pay close attention to the following implicit clues:
*   **Word Choice:** Note the emotional weight of the words the author uses (e.g., describing an action as "fair" vs. "calculated," or a person as "naive" vs. "kind").
*   **Narrative Focus:** What parts of the story does the author spend the most time describing? The details they emphasize reveal what they believe is most important.
*   **Description of Actions:** Analyze the author's behavior and the actions they describe. Actions often reveal priorities more than words do.
*   **Omissions:** What conventional viewpoints or considerations are missing from the narrative? The absence of a principle can be as revealing as its presence.

---
### The Six Moral Dimensions
Here are the six key dimensions of moral reasoning. You are evaluating which of these principles the author seems to value most.

*   **Concern for Others' Well-being (Care/Harm):**
    *   This dimension deals with kindness, compassion, and empathy. It's about whether someone's reasoning focuses on helping others and preventing suffering.
    *   For example, a person focused on this dimension might agree with statements like: "Compassion for those who are suffering is one of the most crucial virtues," or "It pains me when I see someone ignoring the needs of another human being."

*   **Concern for Equality (Equality/Inequality):**
    *   This dimension is about the intuition that all individuals should be treated equally and achieve similar results. Reasoning here focuses on equal treatment and equal distribution of resources.
    *   For example, a person focused on this dimension might agree with statements like: "The world would be a better place if everyone made the same amount of money," or "When people work together toward a common goal, they should share the rewards equally, even if some worked harder on it."

*   **Concern for Proportionality (Proportionality/Cheating):**
    *   This dimension is about the intuition that individuals should be rewarded based on their merits, efforts, or contributions. Reasoning here focuses on people getting what they deserve.
    *   For example, a person focused on this dimension might agree with statements like: "I think people who are more hardworking should end up with more money," or "The effort a worker puts into a job ought to be reflected in the size of a raise they receive."

*   **Concern for Group Loyalty (Loyalty/Betrayal):**
    *   This is about loyalty to a group, like family, friends, a team, or a nation. Reasoning focuses on the importance of sticking together and protecting one's own group.
    *   For example, a person focused on this dimension might agree with statements like: "I think children should be taught to be loyal to their country," or "I believe the strength of a sports team comes from the loyalty of its members to each other."

*   **Concern for Respect & Tradition (Authority/Subversion):**
    *   This dimension deals with respecting legitimate leaders, parents, and traditions. It emphasizes maintaining order and following rules set by authorities.
    *   For example, a person focused on this dimension might agree with statements like: "I believe that one of the most important values to teach children is to have respect for authority," or "We all need to learn from our elders."

*   **Concern for Purity & Sanctity (Sanctity/Degradation):**
    *   This dimension is about the idea that some things are noble or sacred and should be protected from being degraded or treated with disgust.
    *   For example, a person focused on this dimension might agree with statements like: "I think the human body should be treated like a temple, housing something sacred within," or "I believe chastity is an important virtue."

---
### The Rating Scale
Use the following 5-point scale to rate how each dimension is reflected in the author's perspective.

| Score | Meaning             | Description                                                                     |
|-------|---------------------|---------------------------------------------------------------------------------|
| +2    | Main Principle      | This dimension is the primary principle guiding the author's perspective and actions. |
| +1    | Secondary Principle | This dimension is a supporting principle that the author considers, but it is not their main focus. |
|  0    | Not Mentioned       | The author's perspective does not seem to consider or relate to this dimension at all. |
| -1    | Dismissed           | The author acknowledges this dimension but treats it as unimportant in their reasoning. |
| -2    | Actively Opposed    | The author's perspective and actions are based on actively opposing or violating this principle. |

---
### Story for Analysis
{story_text}

---
### Required Output Format
Your entire output must be a single, valid JSON object. The keys must be the string name for each moral dimension, and the value must be the corresponding integer score (-2, -1, 0, +1, or +2). Do not include any explanatory text, comments, or any characters outside of the JSON object.

Example of required output format:
{{
  "Concern for Others' Well-being": 0,
  "Concern for Equality": -2,
  "Concern for Proportionality": 2,
  "Concern for Group Loyalty": 1,
  "Concern for Respect & Tradition": -1,
  "Concern for Purity & Sanctity": 0
}}
"""


# =============================================================================
# AUTHORITY CLASSIFICATION PROMPTS (for Authority dimension splitting)
# =============================================================================
# These prompts classify stories into Family vs Society authority types.
# This enables splitting the Authority dimension into Authority_Family and 
# Authority_Society for more granular analysis.
#
# Classification outputs:
# - "family": Authority within family/interpersonal relationships
# - "societal": Authority within society/institutions  
# - "mixed": Both family and societal authority significantly involved
# - "none": No clear authority relationship in the story

# English prompt for AITA posts
AUTHORITY_CLASSIFICATION_PROMPT_EN = """
Task: Analyze the following story and classify the TYPE OF AUTHORITY involved.

Stories involving moral dilemmas often involve authority relationships. These can be broadly categorized as:

1. **FAMILY AUTHORITY**: Authority within family/interpersonal relationships
   - Examples: parental authority over children, elder authority, sibling dynamics
   - Respect for parents, grandparents, in-laws
   - Family hierarchy and decision-making power
   - Domestic rules and household authority
   - Authority of spouse, partner in relationship decisions

2. **SOCIETAL AUTHORITY**: Authority within society/institutions
   - Examples: boss/manager authority, governmental authority, institutional rules
   - Workplace hierarchy (managers, supervisors, employers)
   - Legal/governmental authority (laws, police, courts)
   - Institutional authority (schools, hospitals, organizations)
   - Professional authority (doctors, teachers, officials)
   - Social norms and community expectations

Story to analyze:
---
{story}
---

Please analyze the story and respond with a valid JSON object:
- `authority_type`: (string) One of: "family", "societal", "mixed", or "none"
  - "family": The main authority conflict/relationship is within family context
  - "societal": The main authority conflict/relationship is within societal/institutional context
  - "mixed": Both family and societal authority are significantly involved
  - "none": No clear authority relationship in the story
- `confidence`: (string) "high", "medium", or "low"
- `reasoning`: (string) Brief explanation (1-2 sentences) for your classification
- `key_authority_figures`: (list) Main authority figures/relationships identified

Example response:
{{
  "authority_type": "family",
  "confidence": "high",
  "reasoning": "The story centers on conflict with the narrator's mother about household rules and parental expectations.",
  "key_authority_figures": ["mother", "parental expectations"]
}}

Another example:
{{
  "authority_type": "societal",
  "confidence": "high", 
  "reasoning": "The conflict involves a manager's decision at work and company policy enforcement.",
  "key_authority_figures": ["manager", "company policy"]
}}
"""

# Chinese prompt for CMoral posts
AUTHORITY_CLASSIFICATION_PROMPT_CN = """
任务：分析以下故事，判断其中涉及的**权威类型**。

涉及道德困境的故事通常包含权威关系。这些可以大致分为两类：

1. **家庭权威**：家庭/人际关系中的权威
   - 例如：父母对子女的权威、长辈权威、兄弟姐妹关系
   - 对父母、祖父母、公婆/岳父母的尊重
   - 家庭等级制度和决策权
   - 家规和家庭权威
   - 配偶、伴侣在关系中的决定权

2. **社会权威**：社会/机构中的权威
   - 例如：老板/经理的权威、政府权威、机构规定
   - 职场等级（经理、主管、雇主）
   - 法律/政府权威（法律、警察、法院）
   - 机构权威（学校、医院、组织）
   - 专业权威（医生、老师、官员）
   - 社会规范和社区期望

待分析的故事：
---
{story}
---

请分析故事并返回一个有效的JSON对象：
- `authority_type`：(字符串) 以下之一："family"、"societal"、"mixed" 或 "none"
  - "family"：主要的权威冲突/关系在家庭范围内
  - "societal"：主要的权威冲突/关系在社会/机构范围内
  - "mixed"：家庭和社会权威都显著涉及
  - "none"：故事中没有明确的权威关系
- `confidence`：(字符串) "high"、"medium" 或 "low"
- `reasoning`：(字符串) 简要解释你的分类理由（1-2句话）
- `key_authority_figures`：(列表) 识别出的主要权威人物/关系

示例响应：
{{
  "authority_type": "family",
  "confidence": "high",
  "reasoning": "故事围绕与母亲关于家规和父母期望的冲突展开。",
  "key_authority_figures": ["母亲", "父母期望"]
}}

另一个示例：
{{
  "authority_type": "societal",
  "confidence": "high", 
  "reasoning": "冲突涉及经理在工作中的决定和公司政策的执行。",
  "key_authority_figures": ["经理", "公司政策"]
}}
"""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_judgment_prompt(story_language: str, thinking_language: str) -> str:
    """
    Get the appropriate judgment prompt based on story and thinking language.
    
    Args:
        story_language: 'en' or 'cn' - the language of the story
        thinking_language: 'en' or 'cn' - the language for reasoning
        
    Returns:
        The appropriate prompt template string
    """
    prompts = {
        ('en', 'en'): JUDGMENT_EN_STORY_EN_THINKING,
        ('en', 'cn'): JUDGMENT_EN_STORY_CN_THINKING,
        ('cn', 'en'): JUDGMENT_CN_STORY_EN_THINKING,
        ('cn', 'cn'): JUDGMENT_CN_STORY_CN_THINKING,
    }
    return prompts.get((story_language, thinking_language), JUDGMENT_EN_STORY_EN_THINKING)


def format_judgment_prompt(prompt: str, title: str, text: str) -> str:
    """Format a judgment prompt with the story title and text."""
    return prompt.format(title=title, text=text)


def format_mfq_prompt(story_text: str) -> str:
    """Format the MFQ rating prompt with a story."""
    return MFQ_RATING_PROMPT.format(story_text=story_text)


def format_translation_prompt(title: str, text: str, direction: str = 'en_to_cn') -> str:
    """
    Format a translation prompt.
    
    Args:
        title: Story title
        text: Story text
        direction: 'en_to_cn' or 'cn_to_en'
        
    Returns:
        Formatted translation prompt
    """
    if direction == 'cn_to_en':
        return TRANSLATION_CN_TO_EN.format(title=title, text=text)
    else:
        return TRANSLATION_EN_TO_CN.format(title=title, text=text)


def format_story_filter_prompt(stories: list) -> str:
    """
    Format the story filtering prompt for batch processing.
    
    Args:
        stories: List of dicts with 'index' and 'story' keys
        
    Returns:
        Formatted filtering prompt
    """
    import json
    return STORY_FILTER_PROMPT.format(input=json.dumps(stories, ensure_ascii=False))


def format_authority_classification_prompt(story: str, language: str = 'en') -> str:
    """
    Format the authority classification prompt with a story.
    
    This prompt classifies stories by authority type (Family vs Society) to enable
    splitting the Authority dimension in MFQ analysis.
    
    Args:
        story: The story text to classify
        language: 'en' for English prompt (AITA), 'cn' for Chinese prompt (CMoral)
        
    Returns:
        Formatted classification prompt
    """
    if language == 'cn':
        return AUTHORITY_CLASSIFICATION_PROMPT_CN.format(story=story)
    else:
        return AUTHORITY_CLASSIFICATION_PROMPT_EN.format(story=story)


# =============================================================================
# EXPECTED OUTPUT KEYS
# =============================================================================

# Keys expected in judgment response JSON
JUDGMENT_KEYS = ['judgment', 'explanation']

# Keys expected in translation response JSON
TRANSLATION_KEYS = ['title', 'text']

# Keys expected in story filter response JSONL
STORY_FILTER_KEYS = ['index', 'label']
STORY_FILTER_LABELS = ['Y', 'N', 'UNSURE']

# Keys expected in MFQ rating response JSON
MFQ_DIMENSION_KEYS = [
    'Concern for Others\' Well-being',
    'Concern for Equality', 
    'Concern for Proportionality',
    'Concern for Group Loyalty',
    'Concern for Respect & Tradition',
    'Concern for Purity & Sanctity'
]

# Mapping from MFQ response keys to internal dimension names
MFQ_KEY_TO_DIMENSION = {
    'Concern for Others\' Well-being': 'Care_Harm',
    'Concern for Equality': 'Equality',
    'Concern for Proportionality': 'Proportionality',
    'Concern for Group Loyalty': 'Loyalty',
    'Concern for Respect & Tradition': 'Authority',  # Split into Authority_Family/Authority_Society in processing
    'Concern for Purity & Sanctity': 'Purity'
}

# Valid authority classification types
AUTHORITY_CLASSIFICATION_TYPES = ['family', 'societal', 'mixed', 'none']

# Keys expected in authority classification response JSON
AUTHORITY_CLASSIFICATION_KEYS = ['authority_type', 'confidence', 'reasoning', 'key_authority_figures']


# =============================================================================
# CONVENIENCE EXPORTS
# =============================================================================

__all__ = [
    # Judgment prompts
    'JUDGMENT_EN_STORY_EN_THINKING',
    'JUDGMENT_EN_STORY_CN_THINKING', 
    'JUDGMENT_CN_STORY_EN_THINKING',
    'JUDGMENT_CN_STORY_CN_THINKING',
    # Translation prompts
    'TRANSLATION_EN_TO_CN',
    'TRANSLATION_CN_TO_EN',
    # Story filtering
    'STORY_FILTER_SYSTEM_PROMPT',
    'STORY_FILTER_PROMPT',
    # MFQ rating
    'MFQ_RATING_PROMPT',
    # Authority classification (for dimension splitting)
    'AUTHORITY_CLASSIFICATION_PROMPT_EN',
    'AUTHORITY_CLASSIFICATION_PROMPT_CN',
    # Helper functions
    'get_judgment_prompt',
    'format_judgment_prompt',
    'format_mfq_prompt',
    'format_translation_prompt',
    'format_story_filter_prompt',
    'format_authority_classification_prompt',
    # Expected keys
    'JUDGMENT_KEYS',
    'TRANSLATION_KEYS',
    'STORY_FILTER_KEYS',
    'STORY_FILTER_LABELS',
    'MFQ_DIMENSION_KEYS',
    'MFQ_KEY_TO_DIMENSION',
    'AUTHORITY_CLASSIFICATION_TYPES',
    'AUTHORITY_CLASSIFICATION_KEYS',
]

