---
{
  "id": "file_8m47zygt",
  "filetype": "document",
  "filename": "module_01_learning_summary",
  "created_at": "2026-09-06T15:35:00.404Z",
  "updated_at": "2026-09-06T15:35:00.404Z",
  "meta": {"location": "/", "tags": [], "categories": [], "description": "", "source": "markdown"}
}
---

# Module 01 Learning Summary

> Study note: This is an AI-assisted study artifact. Before submitting any part of it, I need to verify the sources, revise it in my own words, and include the course-required GenAI disclosure.

## Sources Reviewed

- [Module 1 overview](overview_01.md): objectives 1.1 through 1.4.
- [Module 1 readings list](readings_01.md): required reading scope.
- [Quinn and Bederson (2011)](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf), pp. 1-4, through the start of “Classification Dimensions.”
- [Ackerman (2000)](mod_01_readings/The%20Intellectual%20Challenge%20of%20CSCW-%20The%20Gap%20Between%20Social%20Requirements%20and%20Technical%20Feasibility.pdf), pp. 1-5, through the start of “The Social-Technical Gap in Action.”
- [Zafar et al. (2017)](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf), full paper, pp. 1-10.

The [combined local reading](module_01_combined_required_readings.md) preserves the assigned text and figures in one document.

## Core Summary

Module 1 establishes that human-in-the-loop AI is a system of people, tasks, data, models, and organizational practices. Human computation directs human effort toward a computational problem. Crowdsourcing uses an open call to replace work traditionally assigned to a designated worker. Social computing supports social behavior and interaction through technology, whether or not it serves a computational task. [Quinn and Bederson, pp. 2-3](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf)

The readings show why technical accuracy is insufficient. Ackerman argues that people’s work, roles, incentives, communication, and privacy practices are flexible and contextual, while technical systems represent only part of that complexity. Zafar and colleagues show that a classifier can have acceptable overall accuracy while imposing different error rates on groups. [Ackerman, pp. 1-4](mod_01_readings/The%20Intellectual%20Challenge%20of%20CSCW-%20The%20Gap%20Between%20Social%20Requirements%20and%20Technical%20Feasibility.pdf) [Zafar et al., pp. 1-3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf)

## Key Learnings from the Required Readings

### Human computation has a specific role for people

Quinn and Bederson define human computation as a computational process that uses human abilities for problems computers cannot yet solve reliably. A system qualifies when the problem fits the general paradigm of computation and the system directs the human participation. This distinguishes it from people independently creating, discussing, or choosing work. [Quinn and Bederson, p. 2](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf)

The paper places human computation among related concepts rather than treating the labels as synonyms. A crowdsourcing system can overlap with human computation, but crowdsourcing substitutes an undefined, generally large group for a designated worker. Social computing includes technology-mediated social behavior such as blogs, wikis, and online communities, and its purpose is usually not to perform a computation. Data mining extracts patterns from data; it is not human computation when the system did not direct the creation of the human-generated data it analyzes. Collective intelligence is broader because it concerns groups doing things collectively that appear intelligent. [Quinn and Bederson, pp. 2-4](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf)

Human-computation design must account for participation and quality. Quinn and Bederson identify motivation, human skill, aggregation, quality control, process order, and task-request cardinality as the six factors in their taxonomy. They note that paying workers can recruit participation but may also create incentives to cheat, especially when participants are anonymous. [Quinn and Bederson, p. 4](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf)

### A technically sound system can fail socially

Ackerman calls the mismatch between social requirements and available technical mechanisms the **social-technical gap**. Social activity is flexible, nuanced, and contextual. Technical mechanisms for roles, information sharing, and policy are comparatively rigid, so a system can work as designed and still fail to support how people actually coordinate. [Ackerman, pp. 1-2](mod_01_readings/The%20Intellectual%20Challenge%20of%20CSCW-%20The%20Gap%20Between%20Social%20Requirements%20and%20Technical%20Feasibility.pdf)

The assigned excerpt gives concrete reasons to examine the operating context: people may have multiple or conflicting goals; shared meanings may have to be negotiated; work processes contain normal exceptions; roles can be informal and fluid; awareness can help coordination but create privacy and interruption tradeoffs; and people need ways to negotiate norms, exceptions, and breakdowns. Incentives also shape whether people share information or adopt a collaborative system. [Ackerman, pp. 3-5](mod_01_readings/The%20Intellectual%20Challenge%20of%20CSCW-%20The%20Gap%20Between%20Social%20Requirements%20and%20Technical%20Feasibility.pdf)

For a human-AI system, I should ask whose judgment defines the task, which exceptions the workflow permits, who can challenge a decision, what information is visible to whom, and whether the incentives support careful participation. These are system requirements, not implementation details.

### Fairness depends on the error and the affected group

Zafar et al. distinguish three fairness concepts. **Disparate treatment** occurs when a prediction changes after observing a sensitive attribute when the other features are fixed. **Disparate impact** concerns whether the positive-decision rate differs across sensitive-attribute groups. **Disparate mistreatment** concerns whether groups experience different misclassification rates. [Zafar et al., pp. 2-3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf)

The relevant harm determines the evaluation measure. False-positive and false-negative rates condition on the true class. False-discovery and false-omission rates condition on the predicted class. The paper notes that it can be impossible to satisfy every fairness criterion at once when groups have different positive-class base rates, so selecting a fairness objective is a substantive decision about harms and tradeoffs. [Zafar et al., pp. 3-4](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf)

The authors propose training decision-boundary classifiers with constraints based on the covariance between sensitive attributes and the distance of misclassified examples from the decision boundary. Their formulation uses disciplined convex-concave programming, so it relies on heuristics rather than a guarantee of a global optimum. They report that stricter constraints can reduce disparity while lowering accuracy, and smaller datasets can make the covariance estimate less reliable. [Zafar et al., pp. 4-5, 9](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf)

## Specific Evidence to Remember

| Reading | Specific fact | Why it matters |
| --- | --- | --- |
| Quinn and Bederson | The modern use of “human computation” was influenced by von Ahn’s 2005 dissertation; the first annual Workshop on Human Computation was held in Paris four years later. [p. 1](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf) | The field developed from collaboration among computing, HCI, business, and other disciplines. |
| Quinn and Bederson | About 90% of Mechanical Turk tasks paid $0.10 or less in the cited study. [p. 4](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf) | Compensation affects recruitment, work quality, and incentives to game a task. |
| Ackerman | CSCW research treats exceptions as normal in work processes and recognizes that roles are frequently informal and fluid. [p. 4](mod_01_readings/The%20Intellectual%20Challenge%20of%20CSCW-%20The%20Gap%20Between%20Social%20Requirements%20and%20Technical%20Feasibility.pdf) | Workflow rules need mechanisms for adaptation and escalation. |
| Zafar et al. | In the COMPAS example, the unconstrained logistic-regression classifier had accuracy of 0.668. Its false-positive rates were 0.35 for Black defendants and 0.17 for White defendants; its false-negative rates were 0.31 and 0.61, respectively. [p. 8](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) | Overall accuracy hid materially different error burdens. |
| Zafar et al. | The COMPAS analysis used 2,639 training examples and only Black and White defendants in the reported subset. [p. 8](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) | The result is an illustration of the method, not a complete fairness assessment for every group or deployment context. |

## Assignment Readiness

For the one-page reflection, I should be able to:

- define social computing, crowdsourcing, and human computation, then explain their boundaries and overlap;
- explain why human roles, incentives, exceptions, and communication make an AI system socio-technical;
- choose a decision context and identify which error type creates the relevant harm;
- state what evidence I would collect about group-level outcomes, task quality, and accountability; and
- distinguish a reading-backed factual claim from my own interpretation.

## My Takeaway to Revise

My takeaway is that human-in-the-loop AI is not improved simply by inserting people into an automated workflow. I need to define the human task, examine incentives and exceptions, evaluate the quality of human and model decisions, and decide which fairness harms matter for the people affected. I also need to make those choices reviewable and contestable in the operating context.

## Glossary of Module Terms

| Term | Definition for this module | Source |
| --- | --- | --- |
| **Aggregation** | Combining individual units of human work to produce an answer to the original request. | [Quinn and Bederson, p. 4](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf) |
| **Classification** | Learning a mapping from feature vectors to class labels, then applying it to new examples. | [Zafar et al., p. 3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **Computer-supported cooperative work (CSCW)** | The study of technology used to augment an organization’s social activity. | [Module 1 readings list](readings_01.md) |
| **Collective intelligence** | Groups of individuals doing things collectively that appear intelligent. It is broader than human computation because it includes group activity that is not directed toward a computational task. | [Quinn and Bederson, pp. 3-4](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf) |
| **Crowdsourcing** | Taking a job traditionally performed by a designated worker and offering it to an undefined, generally large group through an open call. | [Quinn and Bederson, p. 3](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf) |
| **Data mining** | Applying algorithms to extract patterns from data. It does not itself become human computation merely because people created the data. | [Quinn and Bederson, p. 3](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf) |
| **Decision boundary** | The boundary in feature space that separates a classifier’s predicted classes. | [Zafar et al., pp. 3-4](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **Disciplined convex-concave programming (DCCP)** | A heuristic optimization approach used in the paper to solve the non-convex fairness-constrained classifier formulation; it does not guarantee a global optimum. | [Zafar et al., pp. 4-5, 9](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **Disparate impact** | A difference between sensitive-attribute groups in the probability of receiving a positive prediction. | [Zafar et al., p. 3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **Disparate mistreatment** | A difference between sensitive-attribute groups in one or more misclassification rates. | [Zafar et al., pp. 2-3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **Disparate treatment** | A prediction depends on a sensitive attribute after the other feature values are fixed. | [Zafar et al., p. 3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **False-discovery rate** | The fraction of positive predictions that are incorrect. | [Zafar et al., p. 3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **False-negative rate** | The fraction of true positive cases incorrectly predicted as negative. | [Zafar et al., p. 3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **False-omission rate** | The fraction of negative predictions that are incorrect. | [Zafar et al., p. 3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **False-positive rate** | The fraction of true negative cases incorrectly predicted as positive. | [Zafar et al., p. 3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **Human computation** | A computational process that directs people to contribute abilities needed to solve a computational problem. | [Quinn and Bederson, p. 2](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf) |
| **Overall misclassification rate** | The proportion of all predictions that are incorrect, evaluated separately for each sensitive-attribute group when assessing disparate mistreatment. | [Zafar et al., p. 3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **Sensitive attribute** | A feature describing group membership that is relevant to a fairness assessment, such as race or gender in the paper’s examples. | [Zafar et al., pp. 2-3](mod_01_readings/Fairness%20Beyond%20Disparate%20Treatment%20%26%20Disparate%20Impact-%20Learning%20Classification%20without%20Disparate%20Mistreatment%201610.08452v2.pdf) |
| **Social computing** | Technology-mediated social behavior and interaction, including blogs, wikis, and online communities. | [Quinn and Bederson, p. 3](mod_01_readings/Human%20Computation,%20A%20Survey%20and%20Taxonomy%20of%20a%20Growing%20Field%20%28CHI%202011%29%20%281%29.pdf) |
| **Social-technical gap** | The gap between what a system must support socially and what its technical mechanisms can support. | [Ackerman, pp. 1-2](mod_01_readings/The%20Intellectual%20Challenge%20of%20CSCW-%20The%20Gap%20Between%20Social%20Requirements%20and%20Technical%20Feasibility.pdf) |
