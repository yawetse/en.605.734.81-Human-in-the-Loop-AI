---
{
  "id": "file_fafz61rp",
  "filetype": "document",
  "filename": "question_3_authorized_usage_reflection",
  "created_at": "2026-09-06T16:03:57.784Z",
  "updated_at": "2026-09-06T16:34:49.023Z",
  "meta": {
    "location": "/",
    "tags": [],
    "categories": [],
    "description": "",
    "source": "markdown"
  }
}
---
# Module 1: One-Page Reflection

**Yaw Etse**\
**Question 3**\
**EN.605.734.81: Human-in-the-Loop AI**\
**September 6, 2026**

<div style="page-break-after: always;"></div>

## Human Control in an Authorized Usage System

**Question 3:** Where should humans remain involved in an AI system, and why?

I apply this question to enterprise data governance through an operating model I have been developing called Authorized Usage, or AuthU. AuthU asks whether data use remains consistent with its approved purpose, context, policy, scope, and evidence requirements. Access controls determine whether a person or system may reach data. AuthU evaluates what happens afterward, including joins, transformations, exports, model training, agent memory, and customer-impacting actions.

AI should perform the repetitive, high-volume work. It can structure a proposed use by purpose, data scope, action, output, audience, and duration. It can compare the request with policies, consent, and contracts; classify its risk; and recommend a permissible path, such as aggregated, masked, synthetic, or differentially private data instead of raw records. During execution, AI can inspect tool calls, capture lineage, detect purpose drift, verify output restrictions, and assemble evidence. These tasks require consistent decisions across more events than people can review manually.

People should control the judgments that establish legitimacy. Business, privacy, legal, risk, and data owners must define permissible purposes and contextual norms. They should decide ambiguous exceptions, conflicting obligations, external disclosures, and uses affecting customer treatment or regulated decisions. People must also determine which errors matter, who bears their cost, when to challenge automation, and who remains accountable. Missing evidence or a material policy conflict should trigger escalation rather than inferred approval.

This division addresses Ackerman's (2000) social-technical gap. Organizational roles, purposes, and exceptions are fluid, while technical controls represent them imperfectly. Nissenbaum's (2004) contextual integrity explains why permission alone is insufficient: an information flow may become inappropriate when its actors, purpose, information type, or transmission conditions change. People interpret those changes; AI applies the resulting rules and identifies deviations at scale.

The design directs human effort toward tasks computers cannot reliably resolve, consistent with Quinn and Bederson's (2011) account of human computation. Effectiveness cannot be measured only by approval speed or aggregate accuracy. Zafar et al. (2017) show that overall performance can conceal different error burdens across groups. I would evaluate inappropriate approvals, unnecessary denials, escalation quality, overrides, and downstream outcomes by group. AuthU becomes responsible human-in-the-loop AI when automation expands safe data use while people retain authority over purpose, exceptions, fairness, and accountability.

<div style="page-break-after: always;"></div>

## References

Ackerman, M. S. (2000). The intellectual challenge of CSCW: The gap between social requirements and technical feasibility. *Human-Computer Interaction, 15*(2-3), 179-203. https://doi.org/10.1207/S15327051HCI1523_5

Nissenbaum, H. (2004). Privacy as contextual integrity. *Washington Law Review, 79*(1), 119-157. https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/

Quinn, A. J., & Bederson, B. B. (2011). Human computation: A survey and taxonomy of a growing field. In *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems* (pp. 1403-1412). Association for Computing Machinery. https://doi.org/10.1145/1978942.1979148

Zafar, M. B., Valera, I., Gomez-Rodriguez, M., & Gummadi, K. P. (2017). Fairness beyond disparate treatment and disparate impact: Learning classification without disparate mistreatment. In *Proceedings of the 26th International Conference on World Wide Web* (pp. 1171-1180). International World Wide Web Conferences Steering Committee. https://doi.org/10.1145/3038912.3052660

World Wide Web Consortium. (2002). *The Platform for Privacy Preferences 1.0 (P3P1.0) specification* (W3C Recommendation, April 16, 2002; obsoleted August 30, 2018). https://www.w3.org/TR/P3P/

ChatGPT-Codex. (2026, September 6). *Drafting and revising an Authorized Usage reflection and P3P appendix* (Yaw Etse, interviewer) \[Generative AI conversation\].

<div style="page-break-after: always;"></div>

## Appendix A: What P3P Shows About the Difficulty of Authorized Usage

> **Generative AI disclosure:** ChatGPT-Codex generated the initial wording of this appendix in response to my request to explain why P3P demonstrates the difficulty of Authorized Usage. The AuthU framework and its underlying concepts come from my prior work. I reviewed the generated material and remain responsible for verifying the sources, revising the analysis, and approving the final submission.

The Platform for Privacy Preferences (P3P) is a useful precedent for AuthU because it attempted to make privacy expectations understandable by software. The W3C standard allowed websites to publish machine-readable statements describing the data they collected, its purposes, recipients, and retention. A user agent could compare those statements with a person's preferences and decide whether to notify the person or permit a data exchange (World Wide Web Consortium, 2002).

P3P also exposed the gap between declaring a policy and controlling behavior. The specification explicitly did not provide a technical mechanism for determining whether a website followed its published policy. W3C later reported limited adoption, cases in which websites copied general policies instead of accurately representing their practices, and no enforcement when a P3P statement differed from actual behavior. P3P 1.1 did not advance beyond a Working Group Note because there was insufficient implementation momentum, and W3C marked P3P 1.0 obsolete in 2018.

That history shows why Authorized Usage is difficult. A machine-readable purpose is necessary, but it is not proof that use remained aligned with that purpose. The system must connect the stated purpose to actual queries, joins, transformations, outputs, recipients, retention, and downstream reuse. It must also preserve context when policies are incomplete or when legitimate exceptions arise. Those judgments cannot be reduced to vocabulary alone.

For AuthU, I take P3P as evidence that policy expression must be paired with execution controls and verifiable evidence. AI can translate policies, compare requested and observed behavior, detect drift, and assemble an audit trail. People must define the meaning of legitimate use, validate whether encoded rules reflect organizational and social expectations, resolve exceptions, and impose accountability. P3P made privacy policies machine-readable. AuthU would need to make authorized use observable, enforceable, and reviewable throughout the data lifecycle.
