# Cross-Cultural Moral Judgment in Large Language Models

**Official code and data repository for the paper:**

> *"Untangling Input Language from Reasoning Language: A Diagnostic Framework for Cross-Lingual Moral Alignment in LLMs"*  
> Nan Li, Bo Kang, Tijl De Bie  
> Findings of the Association for Computational Linguistics: EMNLP 2026

This repository provides everything needed to reproduce our experiments and build upon our work:
- 📊 **Datasets**: Bilingual moral dilemma stories (AITA + CMoral) with MFQ ratings
- 🔧 **Prompts**: All prompt templates used for judgment elicitation, translation, and analysis
- 📈 **Annotations**: Multi-model MFQ ratings across 4 experimental conditions

---

## 🎯 What's in This Repository

| Component | Description |
|-----------|-------------|
| **Story Datasets** | AITA (English→Chinese) and CMoral (Chinese→English) moral dilemmas |
| **MFQ Ratings** | 7-dimension moral foundation ratings from multiple LLMs |
| **Prompt Templates** | Complete prompts for judgment, translation, MFQ rating, and authority classification |

---


## Experimental Design

We test LLMs under **4 conditions** by varying story language and thinking language:

| Condition | Story | Thinking | Purpose |
|-----------|-------|----------|---------|
| EN→EN | English | English | Baseline English reasoning |
| CN→CN | Chinese | Chinese | Baseline Chinese reasoning |
| EN→CN | English | Chinese | Cross-lingual: EN content, CN reasoning |
| CN→EN | Chinese | English | Cross-lingual: CN content, EN reasoning |

---

## 📁 Repository Structure

```
open_source_data/
├── README.md                 # This file
├── prompts.py                # All prompt templates (code)
├── aita_posts.pkl/csv        # AITA stories (EN original + CN translation)
├── cmoral_posts.pkl/csv      # CMoral stories (CN original + EN translation)
├── aita_mfq_en.pkl/csv       # MFQ ratings: AITA English stories
├── aita_mfq_cn.pkl/csv       # MFQ ratings: AITA Chinese translations
├── cmoral_mfq_en.pkl/csv     # MFQ ratings: CMoral English translations
└── cmoral_mfq_cn.pkl/csv     # MFQ ratings: CMoral Chinese stories
```

---

## 🔧 Prompts (`prompts.py`)

All prompts used in our experiments are provided in `prompts.py` for full reproducibility.

### Moral Judgment Elicitation
Four prompts for the 2×2 cross-lingual design:
```python
JUDGMENT_EN_STORY_EN_THINKING  # English story → English reasoning
JUDGMENT_EN_STORY_CN_THINKING  # English story → Chinese reasoning
JUDGMENT_CN_STORY_EN_THINKING  # Chinese story → English reasoning
JUDGMENT_CN_STORY_CN_THINKING  # Chinese story → Chinese reasoning
```

### MFQ Rating
```python
MFQ_RATING_PROMPT  # Rate stories on 6 moral dimensions (Authority split in post-processing)
```

### Authority Classification
Used to split the Authority dimension into Family vs Society:
```python
AUTHORITY_CLASSIFICATION_PROMPT_EN  # For English stories
AUTHORITY_CLASSIFICATION_PROMPT_CN  # For Chinese stories
```

### Translation
```python
TRANSLATION_EN_TO_CN  # Translate AITA posts to Chinese
TRANSLATION_CN_TO_EN  # Translate CMoral posts to English
```

### Story Filtering
```python
STORY_FILTER_PROMPT  # Identify daily moral dilemmas (CMoral curation)
```

### Helper Functions
```python
get_judgment_prompt(story_language, thinking_language)  # Get appropriate judgment prompt
format_mfq_prompt(story_text)                           # Format MFQ rating prompt
format_translation_prompt(title, text, direction)       # Format translation prompt
format_authority_classification_prompt(story, language) # Format authority classification
format_story_filter_prompt(stories)                     # Format batch story filtering
```

---

## 📊 Datasets

### Story Datasets

| Dataset | Posts | Original Language | Source |
|---------|-------|-------------------|--------|
| AITA | 847 (454 YTA + 393 NTA) | English | Reddit r/AmItheAsshole |
| CMoral | 629 | Chinese | Chinese social media |

**Schema:**
| Column | Description |
|--------|-------------|
| `id` | Unique post identifier |
| `en_text` | Story text in English |
| `en_title` | Story title in English |
| `cn_text` | Story text in Chinese |
| `cn_title` | Story title in Chinese |
| `user_verdict` | Ground truth: `Y` (asshole) or `N` (not asshole) |

### MFQ Ratings Datasets

Each story is rated by multiple LLMs on 7 moral dimensions.

**Schema:**
| Column | Description |
|--------|-------------|
| `post_id` | Post identifier (joins with story datasets) |
| `user_verdict` | Ground truth label |
| `dimension` | MFQ dimension (7 total) |
| `<Model>` | Rating from each LLM (-2 to +2) |
| `mean`, `median`, `std` | Aggregate statistics |
| `min`, `max`, `count` | Range and valid count |
| `agreement` | Inter-model agreement |

---

## 🧭 MFQ Dimensions

We use 7 moral dimensions based on Moral Foundations Theory (with Authority split):

| Dimension | Description |
|-----------|-------------|
| **Care_Harm** | Kindness, compassion, preventing suffering |
| **Equality** | Equal treatment and distribution |
| **Proportionality** | Merit-based rewards, fairness |
| **Loyalty** | Group loyalty to family, friends, nation |
| **Authority_Family** | Respect for parental/familial authority |
| **Authority_Society** | Respect for societal/institutional authority |
| **Purity** | Protecting sacred or noble things |

### Rating Scale

| Score | Meaning | Description |
|-------|---------|-------------|
| +2 | Main Principle | Primary principle guiding the author |
| +1 | Secondary | Supporting principle, not main focus |
| 0 | Not Mentioned | Not considered in the narrative |
| -1 | Dismissed | Acknowledged but treated as unimportant |
| -2 | Actively Opposed | Author's actions oppose this principle |

---

## 🚀 Quick Start

### Loading Data

```python
import pandas as pd

# Load story datasets
aita_posts = pd.read_pickle('aita_posts.pkl')
cmoral_posts = pd.read_pickle('cmoral_posts.pkl')

print(f"AITA: {len(aita_posts)} posts")
print(f"CMoral: {len(cmoral_posts)} posts")

# Load MFQ ratings
aita_mfq_en = pd.read_pickle('aita_mfq_en.pkl')
aita_mfq_cn = pd.read_pickle('aita_mfq_cn.pkl')

# Get all ratings for a specific post
post_id = aita_posts['id'].iloc[0]
post_ratings = aita_mfq_en[aita_mfq_en['post_id'] == post_id]
print(post_ratings[['dimension', 'mean', 'median']])
```

### Using Prompts

```python
from prompts import (
    get_judgment_prompt,
    format_mfq_prompt,
    format_authority_classification_prompt
)

# Get judgment prompt for EN story + CN thinking condition
prompt = get_judgment_prompt(story_language='en', thinking_language='cn')

# Format with actual story
story = aita_posts.iloc[0]
formatted_prompt = prompt.format(title=story['en_title'], text=story['en_text'])

# Format MFQ rating prompt
mfq_prompt = format_mfq_prompt(story['en_text'])

# Classify authority type
auth_prompt = format_authority_classification_prompt(story['en_text'], language='en')
```

### Reproducing Analysis

```python
# Compare EN vs CN thinking on same stories
import numpy as np

# Load both conditions
mfq_en = pd.read_pickle('aita_mfq_en.pkl')  # EN story, EN thinking
mfq_cn = pd.read_pickle('aita_mfq_cn.pkl')  # CN story, CN thinking

# Compare Authority dimension across conditions
auth_en = mfq_en[mfq_en['dimension'].str.contains('Authority')].groupby('post_id')['mean'].mean()
auth_cn = mfq_cn[mfq_cn['dimension'].str.contains('Authority')].groupby('post_id')['mean'].mean()

print(f"Authority (EN thinking): {auth_en.mean():.3f}")
print(f"Authority (CN thinking): {auth_cn.mean():.3f}")
```

---

## 📄 File Formats

Both `.pkl` (pickle) and `.csv` formats are provided:
- **`.pkl`**: Faster loading, preserves data types exactly
- **`.csv`**: Human-readable, universal compatibility

---

## 📚 Citation

If you use this code or data, please cite our paper:

```bibtex
@inproceedings{li-etal-2026-untangling,
    title = "Untangling Input Language from Reasoning Language: A Diagnostic Framework for Cross-Lingual Moral Alignment in {LLM}s",
    author = "Li, Nan and Kang, Bo and De Bie, Tijl",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2026",
    month = oct,
    year = "2026",
    address = "Budapest, Hungary",
    publisher = "Association for Computational Linguistics",
}
```

---

## 📜 License

This work is licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

[![CC BY 4.0](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made


