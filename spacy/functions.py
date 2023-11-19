
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




