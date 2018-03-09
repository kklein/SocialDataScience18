Question:
- How do internal and external reactions towards S&P500 index gains/losses differ?

Why ask the question:
- Understand the difference in perception of other people's and own success,
  i.e. obtain a more realistic perspective
- Ability to consciously and actively counteract 'Grass is greener' effect

Hypotheses:
- Internal reactions differ from external reactions
- Internal reaction mirrors loss aversion
- External reaction mirrors survivorship bias

Assumptions (critical for internal validation):
- Reactions to gains/losses in stock are high in arousal (Q1 & Q2)
- #google queries are a proxy internal reaction, e.g. increased or decreased interest
- Reddit comments (frequency or sentiment) are a proxy for external reactions

Roadmap:
- Partition several-year timespan into fine-grained intervals
- Obtain S&P interval data (e.g. wsj), Google Trends interval data, reddit comments (redditExtractoR, PRAW, or reddit dump[1])
  - Critically asses possible constraints to reddit comments in addition to
    including the 'S&P 500' keyword
      e.g. minimal comment length
- Run sentiment analysis on comments
- Fit (possibly non-linear) functions approximating #queries and comments (quantity and average sentiment, separately) from gains
- Fit (possibly non-linear) functions approximating #queries and comments (quantity and average sentiment, separately) from losses
- Internal: 'gain function < loss function' -> loss aversion
- External: 'gain function > loss function' -> survivorship bias
- Regression analysis for fitting of functions
- Validate function difference

[1] http://academictorrents.com/details/85a5bd50e4c365f8df70240ffd4ecc7dec59912b
