# Development Schema — Failure Detective AI

```mermaid
flowchart TD
    A[User describes machine problem] --> B[Streamlit chat interface]
    B --> C[Local Ollama language model]
    B --> D[Symptom recognition]
    D --> E[18-category rule-based knowledge base]
    E --> F[Rank candidate faults using evidence rules]
    F --> G[Show candidate faults and suggested checks]
    G --> H[User performs inspection and submits finding]
    H --> I[Update inspection evidence and rankings]
    I --> G
    F --> J[Diagnostic report and download]
    C --> K[Conversational explanation and follow-up]
    K --> B
```

## Main components
- **Interface:** Streamlit chat and diagnostic workspace.
- **Language model:** Ollama running locally; no hosted paid API is required.
- **Knowledge base:** 18 defined mechanical failure categories with symptoms and checks.
- **Reasoning engine:** rule-based scoring and candidate ranking.
- **Feedback loop:** user-provided inspection findings update the assessment.
- **Output:** chat responses, ranked candidates, inspection guidance, and downloadable report.

## Agent cycle
**Observe → Interpret → Rank → Recommend a check → Receive inspection evidence → Reassess → Report.**
