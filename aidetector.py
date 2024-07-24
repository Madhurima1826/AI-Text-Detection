from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def detect_ai_text(text):
    model_name = "roberta-base-openai-detector"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits

    scores = torch.softmax(logits, dim=1).detach().cpu().numpy()
    ai_score = scores[0][1]
    return ai_score

text = "Snowpipe is good at real-time integration into Snowflake, but it fares poorly with respect to bulk transformations and heterogeneous structured data sources. Alternatives like Apache Kafka or Spark are both strong on complex transformations and have wide compatibility with different data sources. Additonally, the COPY statement in Snowflakes comes out to be more effective than other specialized features in other tools and applications. The choice is now yours.You can also achieve seamless data integration and analytics in Snowflake with Hevo. Don’t know where to start from? We are here to help you. Schedule a demo now."











ai_score = detect_ai_text(text)
print(f"AI Score: {ai_score:.2f}")
