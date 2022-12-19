points_tag = "Important Points and References:"


def title_parser(summary: str):

    start = summary.find("Title:")
    end = summary.find("Summary:")
    return summary[start:end].replace("Title:", "")


def summary_parser(summary: str, title: str):
    print(summary)
    summary_keypoint = summary.replace(title, "").replace("Title:", "")
    summary_keypoint = summary_keypoint.replace("Summary:", "")
    end = summary_keypoint.find(points_tag)
    summary_keypoint = summary_keypoint[:end]
    return summary_keypoint


def keypoint_parser(summary: str):
    try:

        start = summary.find(points_tag)
        keypoints = summary[start:].replace(points_tag, "").strip()
        keypoints = keypoints.split("-")
        try:
            keypoints.remove("")
        except ValueError:
            pass
    except Exception:
        keypoints = ""
    return keypoints


# summary = """\n\nTitle: Exploring Afghanistan: A Journey Through Taliban Country\n\nSummary: In this video, Benjamin takes a journey through Afghanistan to explore the country and gain a better understanding of its people and culture. He visits Kabul, the capital city, where he sees the Taliban flag flying in the breeze. He then travels to Bamyan Province, home to ancient Buddhist ruins that were destroyed by the Taliban. Along his journey he meets locals from different ethnic backgrounds and experiences their hospitality. He also visits an old American military base that was abandoned after US troops pulled out of Afghanistan in 2011. Finally, he stops at a Hazari community where he learns about their liberal views on women's rights despite living under constant threat from Isis and other extremist groups. \n\nImportant Points/Characters: \n- Benjamin - traveler exploring Afghanistan \n- Kabul - capital city with Taliban flags flying \n- Bamyan Province - home to ancient Buddhist ruins destroyed by Taliban \n- Local people from different ethnic backgrounds - friendly hospitality  \n- Old American military base - abandoned after US troops pulled out of Afghanistan in 2011  \n- Hazari community - liberal views on women's rights despite living under constant threat"""
# print(keypoint_parser(summary))
