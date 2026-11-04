from llm_brand_visiblity_v2.schemas import ContextEnum, TypeEnum, IntentEnum

templates = {
    TypeEnum.BRANDED: {
        IntentEnum.BUYING: {
            ContextEnum.BRANDLEVEL: [
                "Where can I buy products from {brand} online?",
                "Are products from {brand} worth buying?",
                "What is the best deal or discount available for {brand} right now?",
            ],
            ContextEnum.PRODUCTLEVEL: [
                "Where can I buy {brand} {product} online?",
                "What is the price of {brand} {product} and is it worth buying?",
                "Best place to order authentic {brand} {product}?",
            ],
            ContextEnum.SERVICELEVEL: [
                "How much does {brand} charge for {service}?",
                "How can I book or hire {brand} for {service}?",
                "Is {brand}'s {service} worth the cost?",
            ],
        },
        IntentEnum.INFORMATIONAL: {
            ContextEnum.BRANDLEVEL: [
                "What is {brand} known for and what do they offer?",
                "Tell me about the company {brand} and its reputation.",
                "Who owns {brand} and what is their background?",
            ],
            ContextEnum.PRODUCTLEVEL: [
                "What are the main features and specifications of {brand} {product}?",
                "How does {brand} {product} work?",
                "What do customer reviews say about {brand} {product}?",
            ],
            ContextEnum.SERVICELEVEL: [
                "What is included in {brand}'s {service}?",
                "How does {brand} deliver its {service} to customers?",
                "What are the terms and turnaround time for {brand} {service}?",
            ],
        },
        IntentEnum.COMPARISON: {
            ContextEnum.BRANDLEVEL: [
                "What are the top alternative brands to {brand}?",
                "How does {brand} compare to other leading brands in the industry?",
                "Is {brand} better than its competitors?",
            ],
            ContextEnum.PRODUCTLEVEL: [
                "What are the best alternatives to {brand} {product}?",
                "How does {brand} {product} compare to other options on the market?",
                "Should I buy {brand} {product} or look for alternatives?",
            ],
            ContextEnum.SERVICELEVEL: [
                "What are alternative providers to {brand} for {service}?",
                "How does {brand}'s {service} compare to other agencies or companies?",
                "Why should I choose {brand} for {service} over competitors?",
            ],
        },
    },
    TypeEnum.UNBRANDED: {
        IntentEnum.BUYING: {
            ContextEnum.PRODUCTLEVEL: [
                "What is the best {product} to buy right now?",
                "Top rated {product} available for purchase today",
                "Where can I find affordable and high-quality {product}?",
            ],
            ContextEnum.SERVICELEVEL: [
                "How to find and hire the best company for {service}?",
                "What is the average cost to purchase professional {service}?",
                "Best providers to hire for {service} this year",
            ],
        },
        IntentEnum.INFORMATIONAL: {
            ContextEnum.PRODUCTLEVEL: [
                "What should I look for before choosing a {product}?",
                "How does a {product} work and what are the benefits?",
                "What are the most common problems to watch out for with a {product}?",
            ],
            ContextEnum.SERVICELEVEL: [
                "What does a professional {service} typically include?",
                "Why would a business or individual need {service}?",
                "How to evaluate whether you need professional {service}",
            ],
        },
        IntentEnum.COMPARISON: {
            ContextEnum.PRODUCTLEVEL: [
                "What are the top 5 brands for {product} compared?",
                "Which brand makes the most reliable {product} on the market?",
                "Compare the leading {product} options currently available",
            ],
            ContextEnum.SERVICELEVEL: [
                "Top companies offering {service} compared by price and quality",
                "Which provider offers the most reliable {service}?",
                "Comparison of the best providers for {service}",
            ],
        },
    },
    TypeEnum.COMPETITOR: {
        IntentEnum.BUYING: {
            ContextEnum.BRANDLEVEL: [
                "Should I buy from {brand} or {competitor}?",
                "Which gives better value for money: {brand} or {competitor}?",
                "Who offers better deals and customer support, {brand} or {competitor}?",
            ],
            ContextEnum.PRODUCTLEVEL: [
                "Should I buy {brand} {product} or {competitor}?",
                "Which is a better purchase: {brand} {product} or {competitor}?",
                "Is {brand} {product} worth paying more for compared to {competitor}?",
            ],
            ContextEnum.SERVICELEVEL: [
                "Should I hire {brand} or {competitor} for {service}?",
                "Which provider gives better pricing for {service}: {brand} or {competitor}?",
                "Is {brand}'s {service} worth it over {competitor}?",
            ],
        },
        IntentEnum.INFORMATIONAL: {
            ContextEnum.BRANDLEVEL: [
                "What is the difference between {brand} and {competitor}?",
                "How do {brand} and {competitor} differ in their approach and quality?",
                "What are the key strengths of {brand} versus {competitor}?",
            ],
            ContextEnum.PRODUCTLEVEL: [
                "What are the key differences between {brand} {product} and {competitor}?",
                "How do specifications of {brand} {product} compare to {competitor}?",
                "What are pros and cons of {brand} {product} versus {competitor}?",
            ],
            ContextEnum.SERVICELEVEL: [
                "How does {brand}'s {service} process differ from {competitor}?",
                "What are the features of {brand} {service} versus {competitor}?",
                "What do customer reviews say about {brand} versus {competitor} for {service}?",
            ],
        },
        IntentEnum.COMPARISON: {
            ContextEnum.BRANDLEVEL: [
                "Compare {brand} vs {competitor}: which brand is better overall?",
                "Detailed comparison between {brand} and {competitor}",
                "Who is the industry leader between {brand} and {competitor}?",
            ],
            ContextEnum.PRODUCTLEVEL: [
                "{brand} {product} vs {competitor}: full comparison and verdict",
                "Head to head: {brand} {product} vs {competitor}",
                "Which should I choose: {brand} {product} or {competitor}?",
            ],
            ContextEnum.SERVICELEVEL: [
                "Compare {brand} vs {competitor} for {service}",
                "Which is better rated for {service}: {brand} or {competitor}?",
                "Feature and quality comparison: {brand} vs {competitor} for {service}",
            ],
        },
    },
}
