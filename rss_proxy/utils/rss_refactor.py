import xml.etree.ElementTree as ElementTree


async def refactor_rss_feed(rss_content):
    # Parse the RSS content
    root = ElementTree.fromstring(rss_content)

    # Iterate over each item in the RSS feed
    for item in root.findall(".//item"):
        description = item.find('description').text
        if description:
            # Find the image URL within the description
            img_start = description.find('<img src="')
            if img_start != -1:
                img_start += len('<img src="')
                img_end = description.find('"', img_start)
                img_url = description[img_start:img_end]
                enclosure = ElementTree.SubElement(item, 'enclosure')
                enclosure.set('url', img_url)
                enclosure.set('type', 'image/jpeg')

    return ElementTree.tostring(root, encoding="utf8", method="xml").decode("utf-8")


if __name__ == '__main__':
    url = "https://nitter.privacydev.net/YinonMagal/rss"
    import requests
    import asyncio
    response = requests.get(url)
    asyncio.run(refactor_rss_feed(response.text))
