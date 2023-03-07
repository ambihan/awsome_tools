# encoding=utf-8
import csv


class LicensePlateChooser(object):
    def __init__(self):
        self.part0_list = list(range(0, 10))
        self.part1_list = list(range(0, 10))
        self.part2_list = ['F']
        self.part3_list = list(range(0, 10))
        self.part4_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
                           'U', 'V', 'W', 'X', 'Y', 'Z']
        self.license_plate_template = '粤B·%d%dF%d%s'

    def get_license_plate(self, part0, part1, part2, part3):
        return self.license_plate_template % (part0, part1, part2, part3)

    @staticmethod
    def get_score_of_license_plate(license_plate):
        license_plate = license_plate[3:]
        char_counts = {x: license_plate.count(x) for x in license_plate}
        # print(char_counts)
        counts_list = list(char_counts.values())
        num_counts = {x: counts_list.count(x) for x in counts_list}
        # print(num_counts)
        score_dict = {
            5: 100,
            4: 50,
            3: 6,
            2: 2,
            1: 0,
        }
        # 基础分数
        score = sum([score_dict[x] * num_counts[x] for x in num_counts])
        # XXXXY/YXXXX加分
        if license_plate[0] == license_plate[1] == license_plate[2] == license_plate[3]:
            score += 2
        if license_plate[1] == license_plate[2] == license_plate[3] == license_plate[4]:
            score += 2
        # XXXYY/YYXXX/XYXYX加分
        if license_plate[0] == license_plate[1] == license_plate[2] and license_plate[3] == license_plate[4]:
            score += 2
        if license_plate[0] == license_plate[1] and license_plate[2] == license_plate[3] == license_plate[4]:
            score += 2
        if license_plate[1] == license_plate[3] and license_plate[0] == license_plate[2] == license_plate[4]:
            score += 2
        # XYZYX加分
        if license_plate[0] == license_plate[4] and license_plate[1] == license_plate[3]:
            score += 2
        # ZXYXY/XYZXY/XYXYZ加分
        if license_plate[1] == license_plate[3] and license_plate[2] == license_plate[4]:
            score += 1
        if license_plate[0] == license_plate[3] and license_plate[1] == license_plate[4]:
            score += 1
        if license_plate[0] == license_plate[2] and license_plate[1] == license_plate[3]:
            score += 1
        # 6、8、9加分
        for x in '689':
            score += license_plate.count(x) * 0.5
        # 4、7减分
        for x in '47':
            score -= license_plate.count(x) * 1
        return score

    def get_scores_of_all_license_plate(self, self_made=False):
        for part0 in self.part0_list:
            for part1 in self.part1_list:
                for part2 in self.part3_list:
                    for part3 in self.part4_list:
                        if self_made and part0 == part1 == part2:
                            continue
                        license_plate = self.get_license_plate(part0, part1, part2, part3)
                        score = self.get_score_of_license_plate(license_plate)
                        yield license_plate, score

    def get_top_license_plates(self, self_made=False, top=None, score_baseline=None):
        license_plate_scores = dict(self.get_scores_of_all_license_plate(self_made))
        print(f'total: {len(license_plate_scores)}')
        sorted_license_plate_scores = sorted(license_plate_scores.items(), key=lambda x: x[1], reverse=True)
        if score_baseline is not None:
            sorted_license_plate_scores = [x for x in sorted_license_plate_scores if x[1] >= score_baseline]
        if top is not None:
            sorted_license_plate_scores = sorted_license_plate_scores[:top]
        return sorted_license_plate_scores


if __name__ == '__main__':
    license_plate_chooser = LicensePlateChooser()
    self_made = True
    top = None
    score_baseline = 4
    top_license_plates = license_plate_chooser.get_top_license_plates(self_made, top, score_baseline)
    with open(f'./results/top_license_plates[{self_made}].csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['license_plate', 'score'])
        writer.writeheader()
        for license_plate, score in top_license_plates:
            writer.writerow({'license_plate': license_plate, 'score': score})
