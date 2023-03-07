# encoding=utf-8
import configparser
import json
import os
import csv


class LicensePlateChooser(object):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')
        self.prefix = self.config['number section']['prefix']
        self.first_section = json.loads(self.config['number section']['first section'])
        self.second_section = json.loads(self.config['number section']['second section'])
        self.third_section = json.loads(self.config['number section']['third section'])
        self.fourth_section = json.loads(self.config['number section']['fourth section'])
        self.fifth_section = json.loads(self.config['number section']['fifth section'])
        self.self_made = self.config['options'].getboolean('self made')
        self.top = int(self.config['options']['top'])
        self.score_baseline = float(self.config['options']['score baseline'])
        self.num_not_liked = json.loads(self.config['ban pick']['num not liked'])
        self.num_liked = json.loads(self.config['ban pick']['num liked'])

    def get_license_plate(self, first, second, third, fourth, fifth) -> str:
        return '%s%s%s%s%s%s' % (self.prefix, first, second, third, fourth, fifth)

    def get_score(self, license_plate: str) -> float:
        license_plate = license_plate[-5:]
        char_counts = {x: license_plate.count(x) for x in license_plate}
        # print(char_counts)
        counts_list = list(char_counts.values())
        num_counts = {x: counts_list.count(x) for x in counts_list}
        score = 0
        # 网上自选号码情况下，有3个以上的数字重复，不算
        if self.self_made and (num_counts.get(3, 0) > 0 or num_counts.get(4, 0) > 0 or num_counts.get(5, 0) > 0):
            return score
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
        for x in self.num_liked:
            score += license_plate.count(x) * 0.5
        # 4、7减分
        for x in self.num_not_liked:
            score -= license_plate.count(x) * 0.5
        return score

    def get_scores_of_all(self):
        for first in self.first_section:
            for second in self.second_section:
                for third in self.third_section:
                    for fourth in self.fourth_section:
                        for fifth in self.fifth_section:
                            license_plate = self.get_license_plate(first, second, third, fourth, fifth)
                            score = self.get_score(license_plate)
                            yield license_plate, score

    def get_top_license_plates(self):
        license_plate_scores = dict(self.get_scores_of_all())
        sorted_license_plate_scores = sorted(license_plate_scores.items(), key=lambda x: x[1], reverse=True)
        sorted_license_plate_scores = [x for x in sorted_license_plate_scores if x[1] >= self.score_baseline]
        sorted_license_plate_scores = sorted_license_plate_scores[:self.top]
        return sorted_license_plate_scores


if __name__ == '__main__':
    license_plate_chooser = LicensePlateChooser()
    top_license_plates = license_plate_chooser.get_top_license_plates()
    print('total:', len(top_license_plates))
    os.makedirs('results', exist_ok=True)
    with open(f'./results/top_license_plates[{license_plate_chooser.self_made}].csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['车牌号', '分数'])
        writer.writeheader()
        for lp, score in top_license_plates:
            writer.writerow({'车牌号': lp, '分数': score})
