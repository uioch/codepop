import re

hz_list  = '零一二三四五六七八九十百千万亿点'
hzf_list = '〇壹贰叁肆伍陆柒捌玖拾佰仟萬億'

def get_number(s):

    s = s.replace('万万', '亿')

    hsub = {}
    for i in range(10):
        hsub[hz_list[i]] = i

    if len(s) <= 0:
        return 0

    if s[0] == '点':
        n1 = 0.0
        f = 1
        for i in range(1, len(s)):
            if s[i] not in hsub:
                raise ValueError(f'{s} [{i}]')
            f *= 0.1
            n1 += hsub[s[i]] * f
        return n1

    #注意：顺序必须从大到小
    hmul = [
        ('点', 0.1),
        ('亿', 100000000),
        ('万', 10000),
        ('千', 1000),
        ('百', 100),
        ('十', 10),
    ]

    n = 0
    for sd, m in hmul:
        ss = s.split(sd)
        if len(ss) > 2:
            raise ValueError(f'{s} {sd}')
        if len(ss) <= 1:
            continue
        
        if sd == '点':
            return get_number(sd + ss[1]) + (get_number(ss[0]) if len(ss[0]) > 0 else 0)
        
        n1 = 0
        if len(ss[1]) == 1 and ss[1] in hsub:
            n1 = get_number(ss[1]) * int(m / 10)
        else:
            n1 = get_number(ss[1])
        
        return n1 + (get_number(ss[0]) if len(ss[0]) > 0 else 1) * m
    
    n = 0
    for c in s:
        if c not in hsub:
            raise ValueError(s)
        n = n * 10 + hsub[c]

    return n

def str_replace(s, single_hanzi = False, fill_zero = 0):

    reg = '['+hz_list+hzf_list+']' + ('+' if single_hanzi else '{2,}')

    hsub = {}
    for i in range(len(hzf_list)):
        hsub[hzf_list[i]] = hz_list[i]

    snew = ''
    spos = 0
    for r in re.finditer(reg, s):
        rs  = s[r.regs[0][0]:r.regs[0][1]]
        rs2 = re.sub('['+hzf_list+']', lambda x: hsub[x.group()], rs)
        #print(r.regs, rs, rs2)

        if spos < r.regs[0][0]:
            snew += s[spos:r.regs[0][0]]
        spos = r.regs[0][1]
        if rs2.replace('点', '') == '':
            snew += rs2
            continue
        rn = get_number(rs2)
        if type(fill_zero) is int and fill_zero > 0 and type(rn) is int:
            snew += ('{:0>'+str(fill_zero)+'d}').format(rn)
        else:
            snew += str(get_number(rs2))
    
    if spos < len(s):
        snew += s[spos:]
    return snew

if __name__ == '__main__':
    test_list1 = [
        '一亿零三百零五万零七十二',
        '四万万',
        '一百万零三亿五千万',
        '一千二百七十九',
        '五十五',
        '四',
        '十',
        '二十',
        '五百',
        '千五',
        '百十',
        '二百五',
        '一千零五',
        '一万零五百零三',
        '一百点三',
        '七点零三五',
    ]
    for s in test_list1:
        print(s, '=>', get_number(s))
    
    s = '三阳开泰四方来财：赚钱一百五十元'
    print(str_replace(s))
    print(str_replace(s, True))
    print(str_replace(s, True, 3))
