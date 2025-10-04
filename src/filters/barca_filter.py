def is_barca_related(text: str) -> bool:
    text = text.lower()
    return any(kw.lower() in text for kw in ["barcelona", "barça", "blaugrana", "camp nou", "la liga"])
  
