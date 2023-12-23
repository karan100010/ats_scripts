
def get_entities(text, nlp):
    doc = nlp(text)
    entities = [
            { 
            "entity": str(i.label_),  
            "text": str(i),
            "label": str(i.label)
            } 
            for i in doc.ents
        ]
    
    
    return entities

def get_sentiment(text, nlp):
    doc = nlp(text)
    sentiments = {
        "polarity": doc._.blob.polarity,
        "subjectivity": doc._.blob.subjectivity,
        "assessments": doc._.blob.sentiment_assessments.assessments
    }

    return sentiments

