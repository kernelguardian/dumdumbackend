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


# summary = 'never gonna run around [Music] and desert you Title: "Never Gonna Say Goodbye" Summary: This song is about a relationship between two people who have known each other for a long time. The singer expresses their feelings of love and commitment to the other person, promising to never let them down or run away. They also vow to never say goodbye, even though their hearts have been aching. Important Points and References: -The singer expresses their feelings of love and commitment to the other person -Promises to never let them down or run away -Vows to never say goodbye, even though their hearts have been aching -The two people have known each other for a long time'
# print(keypoint_parser(summary))
