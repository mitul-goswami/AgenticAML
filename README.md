# 🧠 Agentic AI for Anti-Money Laundering Case Analysis and Reporting (AgenticAML)

An **Agentic AI-based Multi-Agent System** designed to automate **Anti-Money Laundering (AML)** case investigations using **LangGraph** and the **OpenAI API**.  
This system simulates a financial fraud analyst's workflow — parsing case inputs, retrieving data from multiple sources, analyzing patterns, and generating detailed AML case reports with a **Suspicion Score** and **investigative narrative** for **SAR Filing**.

---

## 📘 Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [System Architecture](#system-architecture)
4. [Workflow Description](#workflow-description)
5. [Tech Stack](#tech-stack)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Input Format](#input-format)
9. [Output Format](#output-format)
10. [Agents Description](#agents-description)
11. [Dataset Details](#dataset-details)
12. [Future Enhancements](#future-enhancements)
13. [Contributors](#contributors)
14. [License](#license)

---

## 🧩 Overview

Traditional AML investigations require analysts to manually extract customer and transaction data, review past cases, and generate reports — a process that takes **25–30 minutes per case**.  
The **AgenticAML** system automates this workflow using an **Agentic AI** framework that performs intelligent data parsing, retrieval, and reasoning.  

Using **LangGraph**, multiple agents collaborate autonomously:
- Extracting structured case details  
- Retrieving customer, transaction, and case history data from Excel databases  
- Performing contextual analysis using **LLM reasoning**  
- Generating a **case summary**, **suspicion score (0–100)**, and **detailed justification**

---

## ⚙️ Key Features

- 🧠 **Agentic Multi-Agent System:** Independent agents coordinate tasks for efficient AML case processing.  
- 🔍 **Automated Data Retrieval:** Extracts and integrates data from multiple Excel sources.  
- 🗂 **LLM-Based Reasoning:** Uses OpenAI's API for human-like financial case analysis.  
- 📊 **Suspicion Scoring:** Assigns a score (0–100) indicating the risk level of potential financial misconduct.  
- 📝 **Detailed Reporting:** Generates comprehensive output with a case summary and narrative justification.  
- 🚀 **Productivity Boost:** Reduces average case investigation time from **30 minutes to under 5 minutes**.  

---

## 🏗 System Architecture
```
Input File
    │
    ▼
Input Parser Agent
    │
    ├──► Source System Agent ─┐
    │                          │
    ├──► Transaction Agent ────┤──► LLM Analysis Agent ───► Output Generator
    │                          │
    └──► Case History Agent ───┘
```

Each agent performs a well-defined role and communicates using LangGraph's structured message passing mechanism.

---

## 🔄 Workflow Description

1. **Input Parsing:**  
   The `Input Parser Agent` reads the case text file and extracts details such as Case ID, Customer ID, Account IDs, Transaction IDs, and Previous Case IDs.

2. **Data Retrieval:**  
   - **Source System Agent** → Fetches customer and account details from `Source System Database`.  
   - **Transaction Agent** → Retrieves transaction records for the given Customer ID from `Transaction Database`.  
   - **Case History Agent** → Loads previous case details from `Previous Cases History Database`.  

3. **LLM-Based Analysis:**  
   The `LLM Analysis Agent` integrates the retrieved data and acts as a virtual financial investigator.  
   It detects irregularities in transaction behavior, assesses escalation tiers, and evaluates fraud likelihood.

4. **Report Generation:**  
   The system produces a text file (`OUTPUT.txt`) containing:  
   - **Case Description**  
   - **Suspicion Score (0–100)**  
   - **Detailed Narrative**  

---

## 🧰 Tech Stack

| Component | Description |
|-----------|-------------|
| **Language** | Python 3.10+ |
| **Framework** | LangGraph |
| **LLM API** | OpenAI API |
| **Data Handling** | Pandas, NumPy |
| **File Formats** | Excel (.xlsx), Text (.txt), JSON |
| **Output** | Automated AML Case Report |

---

## 🧑‍💻 Installation
```bash
# Clone the repository
git clone https://github.com/your-username/A2ML-CAR.git
cd A2ML-CAR

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies (`requirements.txt`):**
```
langgraph
openai
pandas
numpy
```

**Set up your OpenAI API key:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

---

## ▶️ Usage

1. Place your input text file as `input_case.txt` in the project root.

2. Ensure Excel data files are named:
   - `large_case_database.xlsx`
   - `transaction_data_sample.xlsx`
   - `case_history_dataset.xlsx`

3. Run the program:
```bash
python main.py
```

4. Output will be generated as:
```
OUTPUT.txt
```

---

## 📄 Input Format

**Example Input (`input_case.txt`):**
```
Case ID: CA6373
Name: Kelly Lee
CustID: CUST9051
Accounts: ACC212, ACC223
Transactions: TXN966
Previous Cases: CA7248
```

---

## 📤 Output Format

**Example Output (`OUTPUT.txt`):**
```
Case Description:
Customer Kelly Lee (CUST9051) shows irregular fund movements between ACC212 and ACC223 during the past month.

Suspicion Score: 72

Detailed Narrative:
Compared to historical averages, recent transactions show a 45% increase in amount and frequency.
Previous case CA7248 was closed at Tier 2, suggesting prior escalation for potential suspicious activity.
Based on behavioral similarity and transaction clustering, this case is likely indicative of layering or structuring activity.
```

---

## 🤖 Agents Description

| Agent | Function |
|-------|----------|
| **Input Parser Agent** | Reads and extracts structured data from the case file. |
| **Source System Agent** | Retrieves customer details and profile information. |
| **Transaction Agent** | Loads transaction records for the given Customer ID. |
| **Case History Agent** | Fetches previous case outcomes and disposition reasons. |
| **LLM Analysis Agent** | Performs analytical reasoning, scoring, and narrative generation. |
| **Output Generator** | Compiles and formats results into a final AML case report. |

---

## 📊 Dataset Details

| Dataset | Purpose | Key Columns |
|---------|---------|-------------|
| `large_case_database.xlsx` | Contains master customer information | CustID, Name, Account, TransactionID, TransactionAmount, Employer, Location, Occupation, Age |
| `transaction_data_sample.xlsx` | Historical transaction data | CustID, Account, Date, Amount |
| `case_history_dataset.xlsx` | Previous AML case details | CaseID, Name, CustID, Accounts, Transactions, Case Disposition Reason, Tier Closed |

---

## 🚧 Future Enhancements

- Integration with real-time transaction monitoring systems
- Support for multi-case batch processing
- Enhanced visual reporting dashboard
- Explainability layer for LLM decision transparency
- Regulatory report automation for SAR submissions

---

## 📜 License

This project is released under the **MIT License**.  
You are free to use, modify, and distribute this software with appropriate credit.

---

⭐ **If you found this project useful, consider giving it a star on GitHub!**
