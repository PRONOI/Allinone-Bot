import emoji

def emoji_tag(item):
    return emoji.emojize(f"🔵🔴 {item['text'][:200]}…\n:link: {item['url']}")
  
