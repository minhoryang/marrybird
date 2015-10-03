__author__ = 'minhoryang'


RESULT_FORM = "당신의 %s 점수는 상위 %s%%입니다."


HEXACO_H = {
    'name': '정직/겸손성',
    'description': '정직/겸손성(Honesty-Humility) 점수에서 높은 점수를 받았다면 돈과 명예에 대한 욕구가 별로 없으므로 개인적인 이득을 위해 다른 사람들을 어떻게 하려 하지 않고 규칙을 지키려고 합니다. 이와는 반대로 낮은 점수를 받았다면 더 앞서가거나 물질적인 이득을 위해 아부를 하고 규칙을 어기는데 어색하지 않으며, 자아존중감이 높습니다.',
    'detail_description': {
        'H:Sinc': '당신의 진실성 점수는 상위 %s%%입니다!\n진실성(Sincerity) 점수는 대인관계에서의 진정성을 의미합니다. 낮은 점수를 받은 사람들은 이득을 위해 남들에게 아부를 떨거나 남들을 좋아하는 척에 익숙하지만, 높은 점수를 받은 사람들은 남들을 조종하고 싶어 하지 않습니다.',
        'H:Fair': '당신의 도덕성 점수는 상위 %s%%입니다!\n도덕성(Fairness) 점수는 부패와 사기 성향을 의미합니다. 낮은 점수를 받은 사람들은 개인적인 이득을 위해 거짓말을 하는 것을 꺼리지 않으나, 높은 점수를 받은 사람들은 남들을 이용해 개인적인 이득을 취하는 것을 피합니다.',
        'H:Gree': '당신의 청렴성 점수는 상위 %s%%입니다!\n청렴성(Greed-Avoidance) 점수는 부와 명예를 중하게 여기는 정도를 의미합니다. 낮은 점수를 받은 사람들은 부와 각종 권리를 누리고 싶어 하지만, 높은 점수를 받은 사람들은 부와 명예가 자신의 원동력이 되지 않습니다.',
        'H:Mode': '당신의 겸손성 점수는 상위 %s%%입니다!\n겸손성(Modesty) 점수는 잘난 체하지 않는 정도를 의미합니다. 낮은 점수를 받은 사람들은 남들보다 자기가 더 나은 사람이라고 생각하여 특권을 누릴 자격이 있다고 생각하지만, 높은 점수를 받은 사람들은 자기 자신을 평범한 사람이라고 생각하여 특별한 대우를 원하지 않습니다.',
    },
    'result_rules': {
        'Total': {
            'avg': 3.33,
            'sd': 0.61,
            'cnt': 40,
        },
        'H:Sinc': {
            'avg': 3.38,
            'sd': 0.74,
            'cnt': 10,
        },
        'H:Fair': {
            'avg': 3.38,
            'sd': 0.99,
            'cnt': 10,
        },
        'H:Gree': {
            'avg': 3.16,
            'sd': 0.90,
            'cnt': 10,
        },
        'H:Mode': {
            'avg': 3.39,
            'sd': 0.74,
            'cnt': 10,
        },
    }
}

HEXACO_E = {
    'name': '정서성',
    'description': '정서성(Emotionality) 점수에서 높은 점수를 받은 사람들은 물리적 위협에 두려움을 느끼며, 인생에 주어지는 스트레스에 불안감을 느껴 다른 사람들의 정서적 도움을 받고 싶어 하며 다른 사람들과의 정서적 애착을 갖습니다. 그에 반해 낮은 점수를 받은 사람들은 물리적 위협에 큰 영향을 받지 않으며 스트레스를 잘 버틸 수 있지만, 걱정거리들을 남들과 나누고 정서적 애착을 갖는데 어색합니다.',
    'detail_description': {
        'E:Fear': '당신의 두려움 점수는 상위 %s%%입니다!\n두려움(Fearfulness) 점수는 두려움에 얼마나 민감하게 반응하는지를 측정합니다. 낮은 점수를 받은 사람들은 다치는 데에 대해 두려워하지 않으며 무신경하지만, 높은 점수를 받은 사람들은 최대한 피하려고 노력합니다.',
        'E:Anxi': '당신의 불안 점수는 상위 %s%%입니다!\n불안(Anxiety) 점수는 비슷한 문제를 겪을 때 얼마나 걱정하는지를 측정합니다. 낮은 점수를 받은 사람들은 어려움을 버텨내는데 크게 힘들어하지 않지만, 높은 점수를 받은 사람들은 작은 문제들에 대해서도 민감하게 반응합니다.',
        'E:Depe': '당신의 의존성 점수는 상위 %s%%입니다!\n의존성(Dependence) 점수는 다른 사람들에게 얼마나 정서적으로 의존되어있는지를 측정합니다. 낮은 점수를 받은 사람들은 자기 자신에 믿음을 가져 혼자서도 문제를 해결할 수 있지만, 높은 점수를 받은 사람들은 조언과 위로를 얻을 수 있는 다른 사람들을 찾습니다.',
        'E:Sent': '당신의 감수성 점수는 상위 %s%%입니다!\n감수성(Sentimentality) 점수는 다른 사람들과 얼마나 정서적으로 연결되어있는지를 측정합니다. 낮은 점수를 받은 사람들은 어떤 사람과 헤어지거나 다른 사람들이 처한 문제들에 대해 무신경하지만, 높은 점수를 받은 사람들은 다른 사람들과 깊은 정서적 관계를 유지하며 다른 사람들의 기분에 대해 공감합니다.',
    },
    'result_rules': {
        'Total': {
            'avg': 3.15,
            'sd': 0.59,
            'cnt': 40,
        },
        'E:Fear': {
            'avg': 2.82,
            'sd': 0.77,
            'cnt': 10,
        },
        'E:Anxi': {
            'avg': 3.31,
            'sd': 0.78,
            'cnt': 10,
        },
        'E:Depe': {
            'avg': 3.13,
            'sd': 0.84,
            'cnt': 10,
        },
        'E:Sent': {
            'avg': 3.35,
            'sd': 0.84,
            'cnt': 10,
        },
    }
}

HEXACO_X = {
    'name': '외향성',
    'description': '외향성(Extraversion) 점수에서 높은 점수를 받은 사람들은 자기 자신을 긍정적으로 받아들이며, 일할 때 자신감을 느끼고 다른 사람들을 이끌 수 있으며, 사람들을 만나고 소통하는 것을 좋아하며, 뭐든지 열심히 하려고 합니다. 그에 반해 낮은 점수를 받은 사람들은 자기 자신을 인기 없는 사람이라 인식하며, 관심이 나에게 집중되는 것을 싫어하고, 인간관계에 무관심하며 비관적인 경향이 있습니다.',
    'detail_description': {
        'X:Expr': '당신의 표현성 점수는 상위 %s%%입니다!\n표현성(Expressiveness) 점수는 모임 안에서 얼마나 자존감을 느끼는가를 측정합니다. 높은 점수를 받은 사람들은 주로 자기 자신에 대해 만족하며 좋은 특징들을 가진 사람이라고 생각하지만, 낮은 점수를 받은 사람들은 무능력함을 느끼는 경우가 많으며 자기 자신에 대하여 인기 없는 사람이라고 생각합니다.',
        'X:SocB': '당신의 사회적 대담성 점수는 상위 %s%%입니다!\n사회적 대담성(Social Boldness) 점수는 여러 종류의 사회에 놓인 개인이 얼마나 편한가, 또는 얼마나 자신감이 있는가를 측정합니다. 낮은 점수를 받은 사람들은 여러 사람 앞에서 말하거나 이끌어야 하는 상황에 놓였을 때 부끄러워하고 어색해하지만, 높은 점수를 받은 사람들은 모르는 사람에게 쉽게 접근하고 모임 안에서 자연스럽게 의견을 피력합니다.',
        'X:Soci': '당신의 사회성 점수는 상위 %s%%입니다!\n사회성(Sociability) 점수는 여러 사람과의 대화 등 사회적 상호작용을 얼마나 즐기는지를 측정합니다. 낮은 점수를 받은 사람들은 주로 혼자서 하는 활동을 좋아하고 굳이 대화하려고 하지 않지만, 높은 점수를 받은 사람들은 사람들과 대화하고 기념일을 챙기거나 친구 집을 방문하는 것을 좋아합니다.',
        'X:Live': '당신의 활력 점수는 상위 %s%%입니다!\n활력(Liveliness) 점수는 주위 일들에 대한 열정과 에너지를 측정합니다. 낮은 점수를 받은 사람들은 열심히 움직이고 밝게 웃는 것이 어색한 일이라고 생각하지만, 높은 점수를 받은 사람들은 주변 사람들로부터 낙관적이고 명랑하다는 평을 많이 듣습니다.',
    },
    'result_rules': {
        'Total': {
            'avg': 3.53,
            'sd': 0.55,
            'cnt': 40,
        },
        'X:Expr': {
            'avg': 2.89,
            'sd': 0.71,
            'cnt': 10,
        },
        'X:SocB': {
            'avg': 2.9,
            'sd': 0.81,
            'cnt': 10,
        },
        'X:Soci': {
            'avg': 3.12,
            'sd': 0.67,
            'cnt': 10,
        },
        'X:Live': {
            'avg': 3.6,
            'sd': 0.62,
            'cnt': 10,
        },
    }
}

HEXACO_A = {
    'name': '원만성',
    'description': '원만성(Agreeableness) 점수에서 높은 점수를 받은 사람들은 그들이 겪은 고통에 대해 용서하고, 남들의 잘못에 대해 자비로우며, 다른 사람들과 같이 협동하기 위한 차분한 상태를 유지하려고 합니다. 그에 반해 낮은 점수를 받은 사람들은 그들이 겪은 고통에 대해 원한을 갖고, 다른 사람들의 부족함에 엄격하게 반응하며, 자신의 주장을 고집스럽게 고수하고, 걸맞지 못한 대우를 받았다고 생각이 든다면 그 자리에서 바로 화를 내는 편입니다.',
    'detail_description': {
        'A:Forg': '당신의 관용성 점수는 상위 %s%%입니다!\n관용성(Forgiveness) 점수는 나 자신에게 해를 끼쳤을 수도 있는 상대방을 얼마나 믿는가를 측정합니다. 낮은 점수를 받은 사람들은 주로 원한관계를 유지하지만, 높은 점수를 받은 사람들은 상대방을 믿을 준비를 하고 언제나 친분을 되돌리고자 합니다.',
        'A:Gent': '당신의 온유성 점수는 상위 %s%%입니다!\n온유성(Gentleness) 점수는 다른 사람들을 대할 때 얼마나 유하고 관대하게 대하는가를 측정합니다. 낮은 점수를 받은 사람들은 다른 사람들을 짜게 평가하는 편이지만, 높은 점수를 받은 사람들은 다른 사람들을 가혹하게 평가하는 것을 싫어하는 편입니다.',
        'A:Flex': '당신의 융통성 점수는 상위 %s%%입니다!\n융통성(Flexibility) 점수는 다른 사람들과 어디까지 타협하고 협력하려고 하는가를 측정합니다. 낮은 점수를 받은 사람들은 자신의 주장을 고집스럽게 끌고 가지만, 높은 점수를 받은 사람들은 다른 사람들과의 논쟁을 피하고 상대방의 주장이 아무리 비이성적이더라도 최대한 받아들여 주기 위해 노력합니다.',
        'A:Pati': '당신의 인내성 점수는 상위 %s%%입니다!\n인내성(Patience) 점수는 주어진 상황에 대해 얼마나 차분함을 유지하는지를 측정합니다. 낮은 점수를 받은 사람들은 작은 일에도 쉽게 화를 내는 편이지만, 높은 점수를 받은 사람들을 화가 나게 하려면 낮은 점수를 받은 사람들보다 훨씬 더 문제를 심각하게 만들어야 합니다.',
    },
    'result_rules': {
        'Total': {
            'avg': 2.81,
            'sd': 0.55,
            'cnt': 40,
        },
        'A:Forg': {
            'avg': 2.59,
            'sd': 0.74,
            'cnt': 10,
        },
        'A:Gent': {
            'avg': 3.14,
            'sd': 0.69,
            'cnt': 10,
        },
        'A:Flex': {
            'avg': 2.57,
            'sd': 0.69,
            'cnt': 10,
        },
        'A:Pati': {
            'avg': 2.99,
            'sd': 0.89,
            'cnt': 10,
        },
    }
}

HEXACO_C = {
    'name': '성실성',
    'description': '성실성(Conscientiousness) 점수에서 높은 점수를 받은 사람들은 그들의 시간과 주변 환경을 체계적으로 정리하며 자신의 목표를 달성하기 위해 꾸준히 노력하는 사람들입니다. 이들은 과업을 완수하는 데 있어 정확함과 완벽을 추구하며, 신중하게 의사 결정을 합니다. 대조적으로, 이 항목에서 낮은 점수를 받은 사람들은 규칙적인 환경과 일정과는 거리가 있으며, 너무 어렵거나 높은 수준의 목표에 도전하는 것을 꺼리는 편입니다. 이들은 자신이 해낸 일에 사소한 오류가 있어도 그냥 넘어가는 경향이 있고, 의사 결정을 하면서 충동적이고, 작은 외부 요인이 결정에 영향을 주기도 합니다.',
    'detail_description': {
        'C:Orga': '당신의 치밀성 점수는 상위 %s%%입니다!\n치밀성(Organization) 점수는 주변 환경에서 일정한 질서를 유지하고자 하는 경향성을 측정합니다. 이 항목에서 낮은 점수를 받은 사람들은 일을 엉성하거나 대충 한다는 평가를 받지만, 이 지표에서 높은 점수를 획득한 사람들은 업무를 치밀하게 처리하며, 작업할 때 계획적으로 처리하는 것을 선호합니다.',
        'C:Dili': '당신의 근면성 점수는 상위 %s%%입니다!\n근면성(Diligence) 점수는 자신에게 주어진 업무에 어느 정도의 노력을 기울이는지를 측정합니다. 이 항목에서 낮은 점수를 받은 사람들은 자신을 되돌아보는 태도가 상대적으로 부족하며, 목표의식이 없다는 이야기를 듣곤 합니다. 반면에 이 항목에서 높은 점수를 받은 사람들은 직업의식이 강하며 자신을 한계치로 밀어붙이는 것을 주저하지 않습니다.',
        'C:Perf': '당신의 완벽성 점수는 상위 %s%%입니다!\n완벽성(Perfectionism) 점수는 업무를 어느 정도로 완벽히, 얼마나 섬세하게 해내는가를 측정합니다. 이 항목에서 낮은 점수를 받은 사람들은 그들의 일에 있어서 사소한 문제를 내버려두거나 꼼꼼하게 살펴보지 않는 경향이 있습니다. 반면에 해당 항목에서 높은 점수를 획득한 사람들은 실수를 미리 방지하는데 주의를 기울이고, 과업의 잠재적 향상 가능성에 대해 주시합니다.',
        'C:Prud': '당신의 신중성 점수는 상위 %s%%입니다!\n신중성(Prudence) 점수는 의식적으로 신중을 기하는 행위나 충동을 억제하는 경향성을 측정합니다. 이 항목에서 낮은 점수를 받은 사람들은 충동적이거나 기분파인 경향이 있지만, 높은 점수를 받은 사람들은 자신에게 주어진 선택들에 대하여 신중히 고려하고, 각종 충동에 대해 자제심을 가지고 주의하는 경향이 있습니다.',
    },
    'result_rules': {
        'Total': {
            'avg': 3.46,
            'sd': 0.50,
            'cnt': 40,
        },
        'C:Orga': {
            'avg': 3.39,
            'sd': 0.77,
            'cnt': 10,
        },
        'C:Dili': {
            'avg': 3.39,
            'sd': 0.66,
            'cnt': 10,
        },
        'C:Perf': {
            'avg': 3.59,
            'sd': 0.67,
            'cnt': 10,
        },
        'C:Prud': {
            'avg': 3.1,
            'sd': 0.71,
            'cnt': 10,
        },
    }
}

HEXACO_O = {
    'name': '개방성',
    'description': '개방성(Openness to Experience) 점수에서 높은 점수를 받은 사람들은 자연과 예술의 아름다움에 대해 개방적인 태도로 받아들이며, 다양한 분야의 지식에 관심이 많습니다. 또한, 그들은 그들의 상상력을 현실 세계에 적용하는 데에 자유로우며, 독특한 아이디어와 사람들에 관심이 많습니다. 대조적으로, 이 항목에서 낮은 점수를 받은 사람들은 예술에 대해 다소 둔감한 편이며, 지적 호기심이 적고, 창조적인 일을 하는 것을 꺼립니다. 또한, 이러한 사람들은 급진적이거나 평범하지 않은 생각들에 대하여 보수적인 견해를 취합니다.',
    'detail_description': {
        'O:AesA': '당신의 심미성 점수는 상위 %s%%입니다!\n심미성(Aesthetic Appreciation) 점수는 자연과 예술품을 감상하며 얼마나 기쁨을 느끼는지 측정합니다. 낮은 점수를 받은 사람들은 자연경관들이나 미술품의 아름다움을 섬세하게 살피려 하지 않지만, 높은 점수를 받은 사람들은 다양한 종류의 예술과 자연경관에 감탄합니다.',
        'O:Inqu': '당신의 지적 호기심 점수는 상위 %s%%입니다!\n지적 호기심(Inquisitiveness) 점수는 자연과 인간 세계에서의 지식과 경험을 얼마나 얻고자 하는지를 측정합니다. 낮은 점수를 받은 사람들은 다양한 종류의 학문에 무관심하지만, 높은 점수를 받은 사람들은 다방면으로 습득하고자 하며 여행에도 관심을 많이 두는 편입니다.',
        'O:Crea': '당신의 창조성 점수는 상위 %s%%입니다!\n창조성(Creativity) 점수는 실험 정신과 혁신에 대한 선호도를 측정합니다. 낮은 점수를 받은 사람들은 독창적인 생각을 하려고 굳이 고민하려 들지 않지만, 높은 점수를 받은 사람들은 자신에게 닥친 문제들에 대해 새로운 해결책을 찾기 위해 노력하고, 예술이라는 매개체를 통해서도 자신을 표현하려고 합니다.',
        'O:Unco': '당신의 비관습성 점수는 상위 %s%%입니다!\n비관습성(Unconventionality) 점수는 특이한 것들에 대해 어디까지 받아들일 수 있는지 측정한다. 낮은 점수를 받은 사람들은 독특한 사람들을 피하지만, 높은 점수를 받은 사람들은 이상하거나 급진적인 아이디어에 대해 수용적인 편입니다.',
    },
    'result_rules': {
        'Total': {
            'avg': 3.39,
            'sd': 0.53,
            'cnt': 40,
        },
        'O:AesA': {
            'avg': 3.31,
            'sd': 0.97,
            'cnt': 10,
        },
        'O:Inqu': {
            'avg': 3.41,
            'sd': 0.77,
            'cnt': 10,
        },
        'O:Crea': {
            'avg': 3.6,
            'sd': 0.87,
            'cnt': 10,
        },
        'O:Unco': {
            'avg': 3.11,
            'sd': 0.66,
            'cnt': 10,
        },
    }
}
