def floor_layout():
    def station(label, left, top, right, bottom):
        return {
            "id": label,
            "x0": left / 20,
            "y0": (600 - bottom) / 12,
            "x1": right / 20,
            "y1": (600 - top) / 12,
        }

    top_bounds = [
        (88, 288), (303, 527), (566, 742), (757, 965),
        (1004, 1124), (1140, 1379), (1394, 1466),
        (1506, 1793), (1808, 2015),
    ]
    middle_bounds = [
        (56, 280), (319, 503), (542, 726), (765, 941),
        (980, 1163), (1203, 1371), (1402, 1602),
        (1634, 1784), (1824, 2015),
    ]
    bottom_bounds = [
        (104, 280), (295, 527), (542, 734), (741, 965),
        (980, 1163), (1179, 1394), (1410, 1593),
        (1609, 1808), (1824, 2015),
    ]
    stations = [
        station(f"BPO{number:02}", left, 35, right, 123)
        for number, (left, right) in enumerate(top_bounds, start=20)
    ]
    for index, (left, right) in enumerate(middle_bounds):
        number = index * 2 + 1
        center = (left + right) / 2
        top = 155 if index in (0, 2, 4, 6) else 139
        bottom = 474 if index == 0 else 466
        stations.extend([
            station(f"BPO{number:02}", left, top, center, bottom),
            station(f"BPO{number + 1:02}", center, top, right, bottom),
        ])
    stations.extend(
        station(f"BPO{number:02}", left, 490, right, 578)
        for number, (left, right) in enumerate(bottom_bounds, start=30)
    )

    infra = []
    for label, color, bounds in [
        ("VÝŤAH", "#0284c7", (88, 52, 113, 84)),
        ("VÝŤAH", "#0284c7", (88, 386, 113, 418)),
        ("VÝŤAH", "#0284c7", (1036, 251, 1060, 283)),
        ("VÝŤAH", "#0284c7", (1943, 52, 1968, 84)),
        ("VÝŤAH", "#0284c7", (1935, 347, 1952, 363)),
        ("SCHODY", "#e11d48", (72, 52, 88, 84)),
        ("SCHODY", "#e11d48", (72, 386, 88, 418)),
        ("SCHODY", "#e11d48", (654, 52, 686, 68)),
        ("SCHODY", "#e11d48", (638, 370, 662, 402)),
        ("SCHODY", "#e11d48", (1099, 52, 1131, 68)),
        ("SCHODY", "#e11d48", (1099, 386, 1116, 418)),
        ("SCHODY", "#e11d48", (1601, 52, 1633, 68)),
        ("SCHODY", "#e11d48", (1585, 378, 1609, 410)),
        ("SCHODY", "#e11d48", (1968, 52, 1984, 84)),
        ("SCHODY", "#e11d48", (1959, 370, 1984, 402)),
        ("PREDÁK", "#ca8a04", (1060, 60, 1084, 76)),
    ]:
        item = station(label, *bounds)
        item["name"] = item.pop("id")
        item["color"] = color
        infra.append(item)

    path = [
        (184, 143), (299, 143), (299, 470), (522, 470),
        (522, 143), (745, 143), (745, 470), (960, 470),
        (960, 143), (1183, 143), (1183, 470), (1390, 470),
        (1390, 143), (1613, 143), (1613, 470), (1804, 470),
        (1804, 139),
    ]
    return (
        stations,
        infra,
        [x / 20 for x, _ in path],
        [(600 - y) / 12 for _, y in path],
    )
