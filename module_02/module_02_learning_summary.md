# Module 02 Learning Summary

> Study note: This is an AI-assisted study artifact. Before submitting any part of it, I need to verify the sources, revise it in my own words, and include the [course-required GenAI disclosure](../course-info/generative-ai-policy.md).

## Sources Reviewed

- [Module 2 overview](overview_02.md) and [required readings](readings_02.md): objectives 2.1 through 2.4 and the assigned reading scope.
- [Lecture 2a: What Is Human Computation?][l2a]
- [Lecture 2b: Architectures of Human Computation][l2b]
- [Lecture 2c: Collective Intelligence][l2c]
- [Lecture 2d: Human Computation in Practice][l2d]
- [Lecture 2e: Designing Human Computation Systems][l2e]
- [Malone, Laubacher, and Dellarocas: Harnessing Crowds: Mapping the Genome of Collective Intelligence][malone], full local PDF, 21 pages including covers and endnotes.
- [Tang, Li, and Xie (2026): Harnessing the Hybrid Intelligence of Crowd and Artificial Intelligence in Group Decision Making for Uncertain Disaster Response][tang], full paper and appendix, 31 pages.
- [von Ahn and Dabbish (2004): Labeling Images with a Computer Game][esp], full paper, eight PDF pages, published as pp. 319-326.

The [combined required reading](module_02_combined_required_readings.md) brings the three papers together with study questions and source visuals. Page references below refer to the PDF viewer's page count. The lecture transcripts do not contain timestamps, so I identify their topics instead.

## Core Summary

My central learning is that human computation depends on how I organize human contributions. I need to specify the problem, divide it into workable tasks, route those tasks to appropriate people or machines, combine the outputs, and check the result. A larger crowd does not resolve ambiguous instructions, missing context, shared bias, or poor incentives. [Lectures 2a and 2b, pipeline and reliability discussions][l2a] [Architecture tradeoffs][l2b]

I distinguish three related ideas. **Human computation** deliberately places human work inside a computational process. **Crowdsourcing** describes how work is offered to a broad group through an open call. **Collective intelligence** describes intelligent group activity. These concepts overlap, but the label alone does not tell me whether a system produces reliable results. [Lecture 2a, related fields][l2a] [Malone, PDF p. 3][m3] [Tang, section 2.1, PDF p. 3][t3]

The readings give me three complementary views. Malone provides a vocabulary for choosing participants, incentives, tasks, and coordination mechanisms. The ESP Game shows how a task can turn a player's incentive to win into useful image labels. Tang shows how crowd reports, AI estimates, optimization, and expert judgment can support a decision while addressing missing information and unequal representation. [Malone, PDF pp. 4-15][m4] [ESP, PDF pp. 2-3][e2] [Tang, sections 3-5][t5]

## Key Learnings from the Lectures

### I need to define the human contribution precisely

Lecture 2a gives three criteria: the human effort is **intentional**, because the system requests it; **productive**, because it returns useful structured output; and **embedded**, because it forms part of the algorithmic pipeline. My practical check is whether removing the human step changes the computation. Merely collecting data that people happened to create does not establish that the system directed their work. [Lecture 2a, three defining elements][l2a]

I should choose problems where human judgment adds value, the work can be divided, the outputs can be recombined, and quality can be checked. Smaller tasks can reduce cognitive load and improve throughput, but excessive decomposition can remove the context needed for a correct answer. I need to define both the task boundary and the method for combining results. [Lecture 2a, suitable problems][l2a] [Lecture 2e, task decomposition][l2e]

### I should select architecture from the task and consequences of error

| Architecture | How it works | Main benefit | Tradeoff I need to manage |
| --- | --- | --- | --- |
| Independent parallel work | Different contributors complete tasks with few dependencies. | High throughput and low coordination cost. | A single incorrect response may pass through unchecked. |
| Redundant parallelism | Multiple contributors complete the same task. | Agreement can improve confidence. | More work and cost; shared errors can survive voting. |
| Hierarchical workflow | Routine cases stay with the broad workforce; uncertain or difficult cases escalate. | Uses expert attention where it matters most. | Escalation rules and reviewer capacity can create bottlenecks. |
| Iterative refinement | Contributors revise an existing result in sequence. | Supports cumulative improvement. | Later contributors may reinforce an earlier error; version history and rollback matter. |
| Divide and conquer | Contributors solve separate parts of a larger problem, then merge them. | Makes a large task manageable. | Partition boundaries and merge rules must preserve consistency. |
| Competition | Contributors propose solutions and a scoring rule selects the best. | Encourages exploration of alternatives. | Contributors may optimize the score without solving the underlying problem. |
| Collaborative network | Contributors communicate and develop a shared result. | Combines distributed knowledge and supports synthesis. | Coordination costs, influence, and groupthink can undermine the outcome. |

Source: [Lecture 2b, architecture examples and tradeoffs][l2b]. These are design tendencies, not guaranteed rankings of accuracy or speed. I can combine patterns, such as parallel annotation followed by hierarchical verification.

### I need useful differences between contributors

Lecture 2c emphasizes **diversity**, **independence**, **decentralization**, and **aggregation**. A crowd can combine different knowledge and offset some individual errors when its judgments contain useful information and are not dominated by shared bias. I should not infer that every crowd outperforms an expert. [Lecture 2c, conditions for collective intelligence][l2c] [Malone, PDF p. 18, averaging and prediction markets][m18]

Communication creates a tradeoff. It helps contributors exchange knowledge and resolve dependencies, but it can also reduce independence. Groupthink creates pressure to conform; information cascades arise when people follow earlier choices despite their own evidence. I need to decide who sees earlier answers, when discussion begins, and how dissent reaches the final decision. [Lecture 2c, failure modes and communication structure][l2c]

### Aggregation and quality control are separate design decisions

| Mechanism | When I would consider it | What I still need to check |
| --- | --- | --- |
| Majority vote | Categorical labels from reasonably reliable, independent contributors. | Agreement may reflect the same misunderstanding. |
| Weighted vote or reliability estimation | Contributors differ in expertise or demonstrated accuracy. | The evidence used to assign weights must be credible and relevant. |
| Averaging | Numerical estimates whose errors are not systematically biased. | A biased sample can produce a precise but wrong average. |
| Consensus | A shared decision or synthesized output requires deliberation. | Agreement can take time and can conceal pressure to conform. |
| Prediction market | Participants have information about an uncertain future quantity or event. | Incentives, participation, and market design shape the estimate. |

Sources: [Lecture 2c, aggregation methods][l2c]; [Lecture 2e, output types and reliability][l2e]; [Malone, PDF pp. 9-10 and 18][m9]. I still need quality controls such as known-answer tasks, redundant responses, expert review, and investigation of disagreement. I should define these before collecting data. [Lecture 2e, quality control][l2e]

### I should evaluate the whole workflow

The lecture cases help me identify reusable choices: Galaxy Zoo illustrates redundant classification; OpenStreetMap illustrates geographic decomposition and revision; Wikipedia illustrates collaborative editing with oversight; and Foldit illustrates a combination of competition, collaboration, and refinement. I treat these as course examples of architecture, rather than a current inventory of each platform's implementation. [Lectures 2b and 2d, case studies][l2d]

My evaluation should include accuracy, coverage, reliability across contributor groups, throughput, cost, and latency. Ethics also changes the design: I need to minimize unnecessary data exposure, examine who receives tasks and whose needs are represented, explain how contributions will be used, and account for compensation and participant burden. [Lecture 2c, evaluation metrics][l2c] [Lecture 2e, ethical design][l2e]

## Key Learnings from the Required Readings

### Malone: map each activity through Who, Why, What, and How

I can use the paper's framework to explain a system at the task level. A **gene** is one answer to a design question for an activity. A **genome** is the combination of these answers across the system. The same platform can contain several combinations. [Malone, PDF pp. 4-5][m4]

| Question | Main alternatives | What I need to decide |
| --- | --- | --- |
| Who? | Hierarchy or crowd. | Does someone assign the work, or can members of the crowd choose to contribute? |
| Why? | Money, love, or glory. | Does participation depend on payment, enjoyment or purpose, or recognition? |
| What? | Create or decide. | Am I asking people to produce an alternative or evaluate/select among alternatives? |
| How, for creation? | Collection or collaboration; contest is a collection subtype. | Can contributions be produced independently, or do they have dependencies? |
| How, for decisions? | Group decision or individual decisions. | Must the result bind the group, or can people use shared information to make different choices? |

Source: [Malone, PDF pp. 5-11][m5]. Group decisions include voting, consensus, averaging, and prediction markets. Individual decisions include markets and social networks.

Linux illustrates why I should separate creation from selection: a crowd can contribute code while a small hierarchy decides what enters a release. Wikipedia can be a collection of articles at one level and a collaboration within an article at another. I should choose the unit of analysis before assigning a label. [Malone, PDF pp. 8 and 12-13][m8]

My takeaway is that I should justify a combination of mechanisms against task dependencies, available knowledge, incentives, and decision authority. The framework is a design aid. Its appendix describes example collection and informal refinement, not a controlled experiment proving that one combination is best. [Malone, Table 5, PDF p. 15][m15] [Appendix, PDF p. 20][m20]

### ESP Game: align the reward with useful work and test the output

Two randomly paired players see the same image and try to enter matching words without communicating. A match earns points and supplies a candidate label. **Taboo words** prevent reuse of established labels and encourage additional descriptions. A **good label threshold** specifies how many pairs must agree before a label is accepted; the reported implementation used one pair. [ESP, PDF pp. 2-3][e2]

The design connects incentive, aggregation, and quality control. Players want a high score, the shared image gives them a basis for agreement, and the server records matches. Random pairing, restrictions on partners' communication, and mechanisms against coordinated cheating support the validity of agreement. These mechanisms do not establish that every agreed label is correct. [ESP, PDF pp. 2-4][e2]

I should distinguish use from evidence of quality. The authors report player activity and repeat participation, then evaluate search results and conduct two small studies of labels. Those findings support the approach within the reported setting. They do not establish universal accuracy, complete image descriptions, or suitability for every population and application. [ESP, PDF pp. 5-6][e5]

### Tang: combine information sources while preserving expert decision authority

The central problem is selective bias in disaster reporting. People with weaker connectivity or access to digital tools may be less visible in a crowdsourcing platform. I cannot treat a low number of posts as proof of low need. [Tang, introduction and section 2.1, PDF pp. 1-3][t1]

I can trace the proposed workflow through six steps:

1. Clean crowdsourced rescue posts and estimate needs by geographic area.
2. Use rescue-worker urgency labels to support BERT classification of unlabeled posts.
3. Combine urgency with social vulnerability features and use a random forest to estimate rescue demand.
4. Represent uncertainty with scenarios drawn from triangular distributions, then reduce them with clustering.
5. Solve stochastic optimization problems to produce feasible dispatch alternatives from crowd and AI estimates.
6. Ask experts to compare alternatives and build a ranking using maximum consensus sequences.

Sources: [Tang, sections 3-5, PDF pp. 5-11][t5]. The crowd reports local conditions, AI estimates patterns and demand, optimization constructs alternatives, and experts retain the final decision role. This is more specific than inserting a human approval step at the end.

I also need to distinguish two forms of agreement. Independent agreement in the ESP Game is evidence about a label. Tang's consensus procedure constructs a shared preference ordering over dispatch alternatives and can request changes to expert preferences. Its worked example assumes experts accept the proposed revisions. A higher consensus score therefore does not independently prove a better rescue outcome. [ESP, PDF p. 2][e2] [Tang, section 4 and model implementation, PDF pp. 9-10 and 14][t9]

Tang makes inclusion measurable through a resource-matching measure for low-connectivity areas. The case also illustrates competing objectives: the alternative with the largest modeled rescue count does not have the largest rescue percentage. I need to examine the underlying demand estimates, the denominator of each metric, and whose needs receive resources. [Tang, section 6.2.1 and Table 10, PDF pp. 14-16][t14]

## Specific Evidence to Remember

| Source | Reported evidence | How I should interpret it |
| --- | --- | --- |
| Malone, appendix, [PDF p. 20][m20] | The database contained 249 examples. The presented framework was the fourth major generation, refined through informal use with students, managers, researchers, and assistants. | A classification and design framework with an explicit development process. |
| ESP, usage statistics, [PDF p. 5][e5] | Between August 9 and December 10, 2003, 13,630 players produced 1,271,451 labels for 293,760 images. More than 80% played on multiple dates. | Evidence of participation and output in the reported deployment. |
| ESP, labeling rate, [PDF p. 5][e5] | A pair averaged 3.89 labels per minute, with standard deviation 0.69. The estimate of labeling 425 million images in 31 days assumed 5,000 people playing continuously and one label per image. | The first result is measured; the large-scale result is a projection, not a completed deployment. |
| ESP, label evaluation, [PDF p. 6][e6] | Each of two separate studies used 15 participants aged 20-25 and 20 images selected from the first 1,023 images with more than five labels. Manual raters judged about 85% of labels useful and 1.7% unrelated. | These percentages come from a limited evaluation sample, not a full-dataset accuracy audit. |
| Tang, case study, [PDF p. 10][t10] | The Xinxiang case covered 152 townships. Of 1,669 collected posts, 145 were removed, leaving 1,524. Rescue workers had marked urgency for 537 posts; 987 were unmarked. | The workflow relies on both human labels and model inference. |
| Tang, Table 5, [PDF p. 14][t14] | Reported F1 was 79.04% for BERT, 75.20% for logistic regression, and 75.16% for SVM. | The gaps are 3.84 and 3.88 percentage points. Aggregate F1 does not by itself quantify lives saved. |
| Tang, Tables 6-7, [PDF p. 14][t14] | With seven features including urgency, random-forest test MSE was 39.7465, MAE 2.9739, and $R^2=0.8240$. Removing urgency gave MSE 98.0567, MAE 4.1359, and $R^2=0.5659$. | The reported ablation supports urgency's predictive contribution in this dataset. |
| Tang, model implementation, [PDF p. 12][t12] and [p. 14][t14] | Five experts evaluated five alternatives. The consensus threshold was 0.65. After assumed preference revisions, consensus was 0.695 and the ranking was $x_3 > x_5 > x_2 > x_1 > x_4$. | The ranking depends on expert weights, the threshold, and the assumed willingness to revise preferences. |
| Tang, stress test, [Table 11, PDF p. 17][t17] | Under the assumed upper-bound demand scenario, modeled rescue counts were 750 for the deterministic model, 882 for stochastic programming, and 855 for robust optimization. Time-window violations were 890, 520, and 210, respectively. | The experiment illustrates a tradeoff under specified assumptions; these are modeled outcomes, not observed rescue totals. |

## Source Details and Limits I Need to Keep Straight

- **Publication dates:** The module list cites Malone as 2009. The PDF has a cover dated March 19, 2010 and an internal title page dated February 2009. I should identify the version I actually cite. [Malone, PDF pp. 1-2][malone]
- **ESP timeline:** Lecture 2a calls the game a 2001 example. The assigned paper reports its public posting in August 2003 and was published in 2004. I use the paper's dates for the reported study. [Lecture 2a][l2a] [ESP, PDF p. 5][e5]
- **Different definitions:** Malone defines collective intelligence broadly as intelligent collective activity; Lecture 2c emphasizes performance beyond an individual. I should describe the lecture's performance goal without making individual outperformance a requirement of Malone's definition. [Malone, PDF p. 3][m3] [Lecture 2c][l2c]
- **Tang's cluster counts:** The prose on PDF p. 12 states three crowd clusters and two AI clusters. Table 8 and the appendix show two crowd and three AI alternatives. I follow the table and appendix for the breakdown and retain this inconsistency as a source issue. [Tang, PDF p. 12][t12] and [p. 14][t14]
- **Evidence boundary:** Tang analyzes the 2021 flood using a retrospective case study; its feature sources include records dated 2022 and 2025. I should not describe the modeled dispatch results as proof that this system operated during the flood. [Tang, PDF pp. 10 and 12][t12]
- **Limits of the lectures:** The captions are auto-generated and contain transcription errors and broad claims about AI capabilities. I use them for the module's design principles and use the papers for their specific study results.

## Assignment Readiness

The [overview](overview_02.md) names “Designing a Human Computation System.” Lecture 2e asks me to choose a novel problem, justify architectural choices, explain tradeoffs and failure modes, and state how I would measure performance after launch. I did not find a separate Module 2 assignment prompt or rubric in the local folder, so this is preparation from the overview and lectures. [Lecture 2e, closing assignment guidance][l2e]

Before drafting, I should be able to explain:

1. **Problem and suitability:** What outcome do I need, and why does human input improve this task?
2. **Decomposition and context:** What does each contributor receive and return, and how do the parts recombine?
3. **Architecture and routing:** Which patterns do I combine, and what triggers escalation?
4. **Recruitment and incentives:** Whose expertise or local knowledge do I need, who might be missing, and what motivates careful work?
5. **Aggregation and validation:** How do I combine responses, handle disagreement, check accuracy, and detect manipulation?
6. **Ethics and authority:** How do I handle privacy, consent, compensation, unequal representation, and responsibility for the final decision?
7. **Evaluation and failure:** Which quality, coverage, latency, cost, and inclusion measures will I track, and which results would make me change the design?

As a self-check, I should be able to explain why three agreeing contributors can still be wrong, why the highest rescue rate may not indicate the most inclusive plan, and why expert consensus is different from verified correctness.

## My Takeaway to Revise

My takeaway is that reliable human-AI work requires explicit choices about tasks, incentives, information flow, aggregation, and decision authority. I need to test whether human and machine contributions improve the result together, identify whose knowledge or needs are missing, and make the design's assumptions visible enough to challenge.

[malone]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf
[tang]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf
[esp]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf
[m1]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=1
[m2]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=2
[m3]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=3
[m4]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=4
[m5]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=5
[m6]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=6
[m7]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=7
[m8]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=8
[m9]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=9
[m10]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=10
[m11]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=11
[m12]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=12
[m13]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=13
[m14]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=14
[m15]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=15
[m16]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=16
[m17]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=17
[m18]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=18
[m19]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=19
[m20]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=20
[m21]: mod_02_readings/Mapping%20the%20Genome%20of%20Collective%20Intelligence%20-%20ssrn-1381502.pdf#page=21
[t1]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=1
[t2]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=2
[t3]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=3
[t4]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=4
[t5]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=5
[t6]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=6
[t7]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=7
[t8]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=8
[t9]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=9
[t10]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=10
[t11]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=11
[t12]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=12
[t13]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=13
[t14]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=14
[t15]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=15
[t16]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=16
[t17]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=17
[t18]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=18
[t19]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=19
[t20]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=20
[t21]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=21
[t22]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=22
[t23]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=23
[t24]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=24
[t25]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=25
[t26]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=26
[t27]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=27
[t28]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=28
[t29]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=29
[t30]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=30
[t31]: mod_02_readings/Risk%20Analysis%20-%202026%20-%20Tang%20-%20Harnessing%20the%20Hybrid%20Intelligence%20of%20Crowd%20and%20Artificial%20Intelligence%20in%20Group%20Decision.pdf#page=31
[e1]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf#page=1
[e2]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf#page=2
[e3]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf#page=3
[e4]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf#page=4
[e5]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf#page=5
[e6]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf#page=6
[e7]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf#page=7
[e8]: mod_02_readings/Labeling%20Images%20with%20a%20Computer%20Game%20-%20985692.985733.pdf#page=8
[l2c]: module_02_lectures/2c%20-%20Collective-Intelligence_Captions_English%20%28United%20States%29.txt
[l2b]: module_02_lectures/2b%20-%20Architectures-of-Human-Computation_Captions_English%20%28United%20States%29.txt
[l2e]: module_02_lectures/2e%20-%20Designing-Human-Computation-Systems_Captions_English%20%28United%20States%29.txt
[l2a]: module_02_lectures/2a%20-%20What-Is-Human-Computation_Captions_English%20%28United%20States%29%20%281%29.txt
[l2d]: module_02_lectures/2d%20-%20Human-Computation-in-Practice_Captions_English%20%28United%20States%29.txt

## Glossary of Module Terms

| Term | Definition for this module | Source |
| --- | --- | --- |
| **Human computation** | A computational process that intentionally requests useful human work as part of its algorithmic pipeline. | [Lecture 2a, defining elements][l2a] |
| **Intentional, productive, embedded** | The system requests the human effort, receives useful structured output, and uses that output within the computation. | [Lecture 2a][l2a] |
| **Crowdsourcing** | Offering work traditionally assigned to designated workers to an undefined public group through an open call. | [Tang, section 2.1, PDF p. 3][t3] |
| **Collective intelligence** | Intelligent collective activity by a group; the lecture examines conditions under which that activity can exceed individual capability. | [Malone, PDF p. 3][m3]; [Lecture 2c][l2c] |
| **Human-computer interaction (HCI)** | The related field concerned with how people interact with computing systems and their interfaces. | [Lecture 2a, related fields][l2a] |
| **Hybrid intelligence** | A workflow that combines human and AI contributions to use their different strengths. | [Tang, PDF pp. 1-3][t1] |
| **Task decomposition** | Dividing a problem into smaller contributions while retaining enough context and a way to recombine results. | [Lecture 2e][l2e] |
| **Coordination or routing** | Assigning work and directing it to contributors or review stages suited to the task. | [Lecture 2b][l2b] |
| **Aggregation** | Combining individual responses into a system output or decision. | [Lecture 2c][l2c] |
| **Independent parallel work** | Performing different tasks concurrently with few dependencies between contributors. | [Lecture 2b][l2b] |
| **Redundant parallelism** | Having several contributors perform the same task to support validation or aggregation. | [Lecture 2b][l2b] |
| **Hierarchical workflow and escalation** | Routing work through levels of review or expertise as uncertainty, difficulty, or risk increases. | [Lecture 2b][l2b] |
| **Iterative refinement** | Improving an existing artifact through successive revisions. | [Lecture 2b][l2b] |
| **Divide and conquer** | Partitioning a large problem into subproblems, solving them, and merging their outputs. | [Lecture 2b][l2b] |
| **Competitive architecture** | Soliciting alternative solutions and using a scoring rule to select among them. | [Lecture 2b][l2b] |
| **Collaborative network** | A structure in which contributors exchange information and jointly build an outcome. | [Lecture 2b][l2b] |
| **Diversity** | Differences in information, perspectives, and problem-solving approaches among contributors. | [Lecture 2c][l2c] |
| **Independence** | Contributors form judgments without simply copying others. | [Lecture 2c][l2c] |
| **Decentralization** | Allowing contributors to apply knowledge held locally rather than requiring all knowledge to pass through one center. | [Lecture 2c][l2c] |
| **Groupthink** | Pressure to conform that suppresses disagreement and alternative judgments. | [Lecture 2c][l2c] |
| **Information cascade** | A pattern in which people follow earlier choices instead of their own evidence. | [Lecture 2c][l2c] |
| **Herd behavior and correlated errors** | Copying others can make judgments fail together, reducing the benefit of combining responses. | [Lecture 2c][l2c] |
| **Majority vote** | Selecting the categorical answer supported by more than half of the votes. | [Lectures 2b and 2c][l2c] |
| **Weighted vote** | Giving contributors different influence according to relevant expertise or reliability. | [Lecture 2c][l2c] |
| **Expectation maximization (EM)** | An iterative estimation approach; the lecture names it as an aggregation option when contributor reliability varies. | [Lecture 2e, aggregation strategies][l2e] |
| **Gold task** | A task with a known answer used to estimate contributor reliability. | [Lecture 2e, quality control][l2e] |
| **Quality control** | Checks that detect or limit errors before contributions become accepted outputs. | [Lecture 2e][l2e] |
| **Accuracy** | How correct the system's outputs are against an appropriate reference. | [Lecture 2c, evaluation][l2c] |
| **Coverage** | How much of the relevant problem space or population the system reaches. | [Lecture 2c, evaluation][l2c] |
| **Reliability** | Consistency of performance across contributors or repeated use. | [Lecture 2c, evaluation][l2c] |
| **Throughput and latency** | Throughput measures completed work over time; latency measures how long a task takes to return a result. | [Lectures 2b and 2c][l2b] |
| **Gene and genome** | A gene is one answer to Who, Why, What, or How for a task; a genome is the system's combination of those building blocks. | [Malone, PDF pp. 4-5][m4] |
| **Hierarchy and crowd genes** | In a hierarchy someone assigns the activity; in a crowd members can choose to undertake it. | [Malone, PDF p. 5][m5] |
| **Money, love, and glory** | Motivations based on financial benefit, enjoyment or social purpose, and recognition, respectively. | [Malone, PDF p. 6][m6] |
| **Create and decide genes** | Create produces something new; decide evaluates or selects alternatives. | [Malone, PDF p. 6][m6] |
| **Collection** | A creation process whose contributions can be produced independently. | [Malone, PDF p. 7][m7] |
| **Contest** | A collection in which one or a few contributions receive a prize or recognition as the best. | [Malone, PDF p. 7][m7] |
| **Collaboration gene** | Joint creation in which important dependencies connect contributors' work. | [Malone, PDF p. 8][m8] |
| **Group decision** | A decision or shared estimate produced from crowd input for the group as a whole. | [Malone, PDF p. 8][m8] |
| **Individual decisions** | Choices informed by crowd input that may differ from person to person. | [Malone, PDF p. 10][m10] |
| **Implicit voting** | Treating actions, such as purchases or views, as votes without an explicit ballot. | [Malone, PDF p. 9][m9] |
| **Consensus** | Agreement by all or essentially all relevant members in Malone's framework; Tang instead defines a weighted threshold for a preference sequence. | [Malone, PDF p. 9][m9]; [Tang, PDF p. 9][t9] |
| **Averaging** | Combining numerical judgments by their mean, with effectiveness dependent on the errors and bias in those judgments. | [Malone, PDF pp. 9 and 18][m18] |
| **Prediction market** | A mechanism in which trading and outcome-based rewards aggregate beliefs about uncertain future events or quantities. | [Malone, PDF p. 10][m10] |
| **Market gene** | Individual buying and selling decisions coordinated through formal exchange. | [Malone, PDF pp. 10-11][m10] |
| **Social network gene** | Individual choices influenced by relationships, trust, or similarity among crowd members. | [Malone, PDF p. 11][m11] |
| **Collaborative filtering** | Inferring relationships from people's past actions to generate personalized recommendations. | [Malone, PDF pp. 11-12][m11] |
| **Taboo word** | An existing ESP image label that players cannot reuse, encouraging additional descriptions. | [ESP, PDF p. 2][e2] |
| **Good label threshold** | The number of independent player pairs required to agree before an ESP label is accepted. | [ESP, PDF pp. 2-3][e3] |
| **Pre-recorded game play** | Replaying a previous player's guesses and timing as a partner for a live ESP player. | [ESP, PDF p. 3][e3] |
| **Selective bias and digital divide** | Distortion caused when unequal access, connectivity, or digital skills make some populations less visible in the collected data. | [Tang, PDF pp. 1-3][t1] |
| **Social vulnerability features** | Indicators used to represent susceptibility to disaster harm and ability to recover, including urgency, socioeconomic conditions, household composition, and infrastructure. | [Tang, Table 1, PDF p. 6][t6] |
| **BERT** | Bidirectional Encoder Representations from Transformers, the pretrained language model used here to classify rescue-post urgency. | [Tang, section 3.2, PDF p. 5][t5] |
| **Percentile rank** | A relative position in an ordered distribution; Tang uses ranks to put vulnerability features on a comparable scale. | [Tang, equation 1, PDF p. 6][t6] |
| **Cross-validation** | Dividing data into subsets, repeatedly training on the other subsets and evaluating on the held-out subset, then combining results. | [Tang, PDF p. 6][t6] |
| **Scenario** | One possible realization of uncertain parameters, associated with a probability in the stochastic model. | [Tang, PDF p. 6][t6] |
| **Triangular distribution and uncertainty parameter** | A distribution specified by lower bound, most likely value, and upper bound; Tang widens the bounds as uncertainty increases. | [Tang, PDF p. 6][t6] |
| **Scenario reduction** | Reducing many sampled possibilities to representative scenarios using clustering. | [Tang, PDF pp. 6-7][t7] |
| **Stochastic programming (SP)** | Optimizing a decision while accounting for uncertain parameters through probability-weighted scenarios. | [Tang, PDF pp. 6-8][t6] |
| **Robust optimization (RO)** | Optimizing against worst-case parameter realizations within a specified uncertainty set. | [Tang, section 6.2.3, PDF p. 16][t16] |
| **Group decision making (GDM)** | A process in which multiple experts assess alternatives and work toward a collective decision. | [Tang, section 4, PDF p. 9][t9] |
| **Reciprocal preference relation (RPR)** | Pairwise preference scores where opposite-direction preferences sum to one and 0.5 indicates indifference. | [Tang, PDF p. 9][t9] |
| **Consensus threshold and maximum consensus sequence** | A threshold specifies sufficient weighted support; the algorithm builds and extends preference sequences that meet it, with revisions when the ranking is incomplete. | [Tang, PDF pp. 9-10][t9] |
| **Resource matching degree for low-connectivity areas** | The low-connectivity share of modeled rescues divided by its share of modeled demand. One indicates proportional allocation; values below one indicate underrepresentation. | [Tang, section 6.2.1, PDF p. 15][t15] |
