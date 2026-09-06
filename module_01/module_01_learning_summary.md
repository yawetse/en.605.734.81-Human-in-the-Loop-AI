# Module 01 Learning Summary

> Study note: This is an AI-assisted summary of the local Module 01 materials. I need to verify it against the course sources and revise it with my own analysis before using any part of it in a submission. The course policy requires disclosure of GenAI use for submitted work.

## Sources Reviewed

- `overview_01.md`
- `readings_01.md`
- `Module 1 Introduction_Captions_English (United States).txt`
- `Defining the Topic_Captions_English (United States).txt`
- `Socio Technical Systems_Captions_English (United States).txt`
- `Responsible AI_Captions_English (United States).txt`
- Quinn and Bederson, *Human Computation: A Survey and Taxonomy of a Growing Field*
- Ackerman, *The Intellectual Challenge of CSCW: The Gap Between Social Requirements and Technical Feasibility*
- Zafar et al., *Fairness Beyond Disparate Treatment & Disparate Impact: Learning Classification without Disparate Mistreatment*

## Core Summary

Module 01 introduces human-in-the-loop AI through social computing, crowdsourcing, and human computation. I learned that a useful AI system is not only a model. Its results depend on the people who define tasks, label data, review outputs, and act on decisions.

Human computation uses people to complete well-defined computational tasks that machines cannot reliably perform, such as labeling, classification, transcription, and judgment. In a human-computation system, the system directs this human effort toward a computational goal.

Crowdsourcing distributes an open task to a large group. It can provide speed, availability, a range of perspectives, and more reliable aggregate estimates. However, it also requires task design and quality controls because participants can make errors, misunderstand instructions, or introduce systematic bias.

Social computing examines social behavior and interaction mediated by technology. Social media is one form of social computing, but social computing is broader than social media and does not need to serve a computational task. Collective intelligence describes the useful results that can emerge from a group, although groups can also amplify harmful behavior or poor information.

## Key Learnings

1. **Human computation, crowdsourcing, and social computing overlap but are not interchangeable.** Quinn and Bederson distinguish human computation, which directs human effort to solve computational problems, from crowdsourcing, which uses an open call to replace work otherwise performed by designated workers. Social computing supports social interaction through technology.

2. **The human process constrains model performance.** The introductory lecture gives an example in which inconsistent human triage labels limited classifier performance. Improving the standards used by people to label and triage the work improved the resulting system. I should evaluate label quality, task instructions, reviewer consistency, and feedback loops before assuming that a model change is the correct solution.

3. **Human-AI systems are socio-technical systems.** Ackerman's social-technical gap explains why real social requirements and work practices may not fit the technical solution available. A system can perform well in a narrow technical evaluation but still fail when it conflicts with organizational processes, user needs, incentives, or accountability.

4. **Accuracy alone is not a sufficient evaluation measure.** The responsible AI lecture and the Zafar et al. reading show that outcomes and error rates may differ across groups. Relevant concepts include disparate treatment, disparate impact, and disparate mistreatment. I should identify the relevant fairness measure and examine group-level error patterns, not only overall accuracy.

5. **Bias can enter at several points in the system.** Potential sources include the people selected to label data, labeling guidance, unrepresentative data, model design, decision thresholds, and the operational use of outputs. Content moderation illustrates the need to evaluate both human reviewers and automated flagging systems.

## Assignment Readiness

For the Module 01 one-page reflection, I should be prepared to:

- define social computing, crowdsourcing, and human computation in my own words;
- distinguish crowdsourcing from human computation and explain where they overlap;
- describe how social media relates to social computing;
- explain why a human-AI system needs evaluation of people, data, model behavior, and governance; and
- use a concrete example, such as content moderation or data labeling, to identify a benefit, a risk, and an appropriate control.

## Draft Takeaway to Revise

My takeaway is that human-in-the-loop AI requires more than adding a person to an automated workflow. I need to define the human role, provide clear task standards, measure the quality and fairness of the outputs, and establish responsibility for decisions. When performance is weak, I should examine the human process and the data as well as the model.
