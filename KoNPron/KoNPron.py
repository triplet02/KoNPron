class KoNPron:
    def __init__(self):
        self.base_digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.super_digit = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
        self.small_scale = ['', '십', '백', '천']
        self.large_scale = ['', '만 ', '억 ', '조 ', '경 ', '해 ']
        self.literal = ['영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구']
        self.spoken_unit = ['', '하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉']
        self.spoke_tens = ['', '열', '스물', '서른', '마흔', '쉰', '예순', '일흔', '여든', '아흔']
        self.sentence = str()

    def _detect(self, sentence):
        self.sentence = sentence
        detection_data = list()
        tmp = str()

        total_len = len(sentence)
        point_count = 0
        continuous_count = 0
        digit_type = 'vanilla'

        detected = False
        zero_started = False

        for idx, char in enumerate(sentence):
            if char in self.base_digit:
                if not detected:
                    detected = True
                    if char is '0':
                        zero_started = True
                tmp += char
                continuous_count += 1
                if zero_started and continuous_count > 8:
                    digit_type = 'telephone/none'
                if continuous_count > 20:
                    digit_type = 'enormous/none'
            else:
                continous_count = 0
                zero_started = False
                if char == ',':
                    if idx + 1 < total_len and idx > 0:
                        if sentence[idx - 1] in self.base_digit and sentence[idx + 1] in self.base_digit:
                            tmp += char
                elif char == '.':
                    if idx + 1 < total_len and idx > 0:
                        if sentence[idx - 1] in self.base_digit and sentence[idx + 1] in self.base_digit:
                            point_count += 1
                            if point_count == 1:
                                digit_type = 'fraction'
                            if point_count > 1:
                                digit_type = 'version'
                            tmp += char
                elif char == '^':
                    if idx + 1 < total_len and idx > 0:
                        if sentence[idx - 1] in self.base_digit and sentence[idx + 1] in self.base_digit:
                            digit_type += '/square'
                            tmp += char
                        else:
                            if digit_type != 'exception/none':
                                digit_type = 'exception/none'
                                tmp += char
                elif char in self.super_digit:
                    if idx > 0:
                        if sentence[idx - 1] in self.base_digit or sentence[idx - 1] in self.super_digit:
                            if not 'square' in digit_type:
                                digit_type += '/square'
                            tmp += char
                        else:
                            if digit_type != 'exception/none':
                                digit_type = 'exception/none'
                                tmp += char
                elif char == '·':
                    if idx + 1 < total_len and idx > 0:
                        if sentence[idx - 1] in self.base_digit and sentence[idx + 1] in self.base_digit:
                            digit_type = 'date'
                            tmp += char
                else:
                    if detected:
                        detected = False
                        if '/' not in digit_type:
                            digit_type += '/none'
                        detection_data.append((digit_type, tmp))
                        tmp = str()
                        digit_type = 'vanilla'
                        point_count = 0
                        continuous_count = 0
                    else:
                        if tmp:
                            detection_data.append((digit_type, tmp))
                            tmp = str()
                            digit_type = 'vanilla'
                            point_count = 0
                            continuous_count = 0

        if detected:
            if '/' not in digit_type:
                digit_type += '/none'
            detection_data.append((digit_type, tmp))

        elif tmp:
            detection_data.append((digit_type, tmp))
        return detection_data

    def _preprocess(self, detection_data):
        preprocessed_data = list()

        for digit_type, target in detection_data:
            original = target
            target_seq = list()
            reading_method = list()
            target_len = len(target)

            main_type, sub_type = digit_type.split('/')
            if main_type == 'exception':
                return None

            if main_type == 'version':
                splited = target.split('.')
                for count, frag in enumerate(splited):
                    target_seq.append(frag)
                    reading_method.append('individual')
                    if count < len(splited) - 1:
                        target_seq.append('.')
                        reading_method.append('point')
                preprocessed_data.append((reading_method, target_seq, original))

            if main_type == 'date':
                target = target.split('·')
                for frag in target:
                    target_seq.append(frag)
                    reading_method.append('individual')
                preprocessed_data.append((reading_method, target_seq, original))

            if main_type == 'telephone' or main_type == 'enormous':
                target = target.replace('0', '_')
                target_seq.append(target)
                reading_method.append('individual')
                preprocessed_data.append((reading_method, target_seq, original))

            if sub_type != 'none':
                if main_type == 'vanilla':
                    target = [target.replace(',', '')]
                if main_type == 'fraction':
                    target = target.split('.')

                if sub_type == 'square':
                    if '^' not in target[-1]:
                        super_part = str()
                        for idx, digit in enumerate(target[-1]):
                            if digit not in self.base_digit:
                                super_idx = idx
                                break
                        super_num = list(target[-1][idx:])
                        for idx in range(len(super_num)):
                            super_num[idx] = str(self.super_digit.index(super_num[idx]))
                        super_num = ''.join(super_num)
                        super_part += target[-1][:super_idx] + '^' + super_num
                        if main_type == 'vanilla':
                            target = [super_part]
                        else:
                            target = target[:1] + [super_part]
                    if main_type == 'fraction':
                        target_seq.append(target[0])
                        reading_method.append('literal')
                        target_seq.append('.')
                        reading_method.append('point')

                    tmp_len = len(target_seq)
                    tmp = target[-1].split('^')
                    for seq in tmp:
                        target_seq.append(seq)
                        if 'point' in reading_method:
                            if 'of' in reading_method:
                                reading_method.append('literal')
                            else:
                                reading_method.append('individual')
                        else:
                            reading_method.append('literal')
                        if len(target_seq) == tmp_len + 1:
                            target_seq.append("^")
                            reading_method.append("of")
                        elif len(target_seq) == tmp_len + 3:
                            target_seq.append("^")
                            reading_method.append("super")
                    preprocessed_data.append((reading_method, target_seq, original))

            else:
                if main_type == 'vanilla':
                    target = target.replace(',', '')
                    target_seq.append(target)
                    reading_method.append('literal')
                    preprocessed_data.append((reading_method, target_seq, original))

                if main_type == 'fraction':
                    target = target.split('.')
                    for frag in target:
                        target_seq.append(frag)
                        if 'point' in reading_method:
                            reading_method.append('individual')
                        else:
                            reading_method.append('literal')
                        if len(target_seq) == 1:
                            target_seq.append(".")
                            reading_method.append('point')

                    preprocessed_data.append((reading_method, target_seq, original))

        return preprocessed_data

    def _read(self, preprocessed_data, mode='informal'):
        def __literal_read(self, frag, mode='informal'):
            korean = str()
            tmp = str()
            length = len(frag)
            for idx, digit in enumerate(frag):
                digit = int(digit)
                inversed_idx = length - idx - 1
                if mode == 'formal':
                    if inversed_idx % 4:
                        if digit:
                            tmp += self.literal[digit]
                            tmp += self.small_scale[inversed_idx % 4]
                    else:
                        if digit or length == 1:
                            tmp += self.literal[digit]
                        if tmp:
                            tmp += self.large_scale[inversed_idx // 4]
                        korean += tmp
                        tmp = str()

                elif mode == 'informal':
                    if inversed_idx % 4:
                        if digit > 1:
                            tmp += self.literal[digit]
                        if digit:
                            tmp += self.small_scale[inversed_idx % 4]
                    else:
                        if digit or length == 1:
                            tmp += self.literal[digit]
                        if tmp:
                            tmp += self.large_scale[inversed_idx // 4]
                        if length == 5 and digit == 1 and inversed_idx == 4:
                            tmp = tmp[1:]
                        korean += tmp
                        tmp = str()
            korean += tmp
            return korean

        def __individual_read(self, frag):
            korean = str()
            for digit in frag:
                if digit == '_':
                    korean += '공'
                else:
                    korean += self.literal[int(digit)]
            return korean

        result = self.sentence
        if preprocessed_data is None:
            return None

        for each in preprocessed_data:
            reading_method, target_seq, original = each
            readed = str()
            for idx, frag in enumerate(target_seq):
                if reading_method[idx] == 'literal':
                    readed += __literal_read(self, frag)
                if reading_method[idx] == 'individual':
                    readed += __individual_read(self, frag)
                if reading_method[idx] == 'point':
                    readed += ' 점 '
                if reading_method[idx] == 'of':
                    readed += '의 '
                if reading_method[idx] == 'super':
                    readed += ' 승'
            result = result.replace(original, readed, 1)
        return result

    def convert(self, sentence):
        return self._read(self._preprocess(self._detect(sentence)))