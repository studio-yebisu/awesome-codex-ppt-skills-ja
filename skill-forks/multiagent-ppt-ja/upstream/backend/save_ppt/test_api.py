#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2025/7/17 15:13
# @File  : test_api.py.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  :

import requests
import json
import os
import time

# --- 配置 ---
BASE_URL = "http://localhost:10021"  # FastAPI 应用运行的地址
OUTPUT_TEST_DIR = "downloaded_ppts"  # 下载生成的PPT到此目录
TEST_DATA_FILE = "test_ppt_data.json"  # 存储测试JSON数据的文件

# 确保测试输出目录存在
if not os.path.exists(OUTPUT_TEST_DIR):
    os.makedirs(OUTPUT_TEST_DIR)


# 注意：这里需要一个顶层字典，包含 'sections' 和 'references' 键
front_data = [
    {
        "id": "8nJVwBp86wBXHnjf4n6Pl",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "Introduction to Tesla Motors"
                    }
                ],
                "id": "ZigbEk0pDa"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "研究主题"
                                    }
                                ],
                                "id": "SvHtGLhhhA"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉汽车公司的背景、历史和其在汽车行业的意义。"
                                    }
                                ],
                                "id": "giy9t5HNCg"
                            }
                        ],
                        "id": "TEkXhPZR3H"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "子问题拆解"
                                    }
                                ],
                                "id": "rTL7eI0msg"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "包括特斯拉的起源与发展历程、技术突破与市场地位、对传统汽车工业的影响以及未来的发展潜力与挑战。"
                                    }
                                ],
                                "id": "uhRwtMK5sW"
                            }
                        ],
                        "id": "4bOUOgNEQW"
                    }
                ],
                "id": "42w6LOyNtd"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Tesla car",
            "url": "https://cdn.pixabay.com/photo/2024/12/18/07/57/aura-9274671_640.jpg",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "ZBZE7AG3vQEucmtTqsgAW",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉的市场地位与竞争分析"
                    }
                ],
                "id": "iJpwM0hq3o"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "市场份额"
                                    }
                                ],
                                "id": "qup7hHjvjs"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "根据2023年的数据，特斯拉在全球电动车市场的占有率约为15%，位居前列。"
                                    }
                                ],
                                "id": "JHh50y9f0R"
                            }
                        ],
                        "id": "iXhGmjEWjz"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "主要竞争对手"
                                    }
                                ],
                                "id": "dqCoOJbxSX"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "比亚迪、蔚来、宝马和大众等品牌在电动车市场中占据重要位置。"
                                    }
                                ],
                                "id": "SJ3fZdgs4_"
                            }
                        ],
                        "id": "VO1ifHwTbK"
                    }
                ],
                "id": "DlJf720Q5X"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Tesla market position",
            "url": "https://c-ssl.duitang.com/uploads/blog/202111/27/20211127170036_ecc10.png",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "Uvao5htlAoNDrrPAb0-DP",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉的技术突破与市场地位"
                    }
                ],
                "id": "cDAtjVv-GY"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "技术突破"
                                    }
                                ],
                                "id": "Kdxr0Y7szM"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉在电池技术、自动驾驶系统（Autopilot）和软件更新方面具有显著优势。"
                                    }
                                ],
                                "id": "6IwSQCvPOw"
                            }
                        ],
                        "id": "EUcuywljYH"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "市场地位"
                                    }
                                ],
                                "id": "kL2OKt_WBY"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉在全球电动车市场中占据领先地位，凭借技术创新、品牌影响力和垂直整合模式建立了显著的竞争优势。"
                                    }
                                ],
                                "id": "090kJjLVcB"
                            }
                        ],
                        "id": "Uu6AxAwSwu"
                    }
                ],
                "id": "AE2uQeh6hp"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Tesla technology and market position",
            "url": "https://n.sinaimg.cn/spider20250621/120/w1440h1080/20250621/f8d9-7d234d7b43fda7ec916d01fb81555bae.jpg",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "RH_pGO5PnCWXzNXNoQmDI",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉的可持续发展与环境影响"
                    }
                ],
                "id": "l1riZ-6GSg"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "减少碳足迹"
                                    }
                                ],
                                "id": "4fhg4XV0l5"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉通过制造电动汽车减少了传统燃油车的碳排放，尤其是在电力来源清洁的地区，其全生命周期碳排放显著低于燃油车。"
                                    }
                                ],
                                "id": "DOK4Ws-nI4"
                            }
                        ],
                        "id": "EqWLFcVAjn"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "推动可再生能源"
                                    }
                                ],
                                "id": "ugDNFCJwin"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉开发了太阳能产品和储能系统，鼓励用户采用清洁能源。公司致力于建设全球范围内的超级充电站，并逐步转向使用可再生能源供电。"
                                    }
                                ],
                                "id": "jAPWqlhq00"
                            }
                        ],
                        "id": "CxW3-jDihT"
                    }
                ],
                "id": "CmPoEt9TBE"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Battery degradation curve",
            "url": "https://n.sinaimg.cn/spider20250610/598/w955h443/20250610/d5d4-b0eb5848953ded18fbc44aefb452923d.png",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "5uyW3JgOeD9ZbEFB_2iW_",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉面临的挑战与未来前景"
                    }
                ],
                "id": "y2QFM73QyV"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "主要挑战"
                                    }
                                ],
                                "id": "q1dtux9SFi"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉面临的主要生产瓶颈包括工厂产能受限、自动化生产线故障频发，以及供应链问题如芯片短缺和电池材料供应不足。"
                                    }
                                ],
                                "id": "M2egHQqaSe"
                            }
                        ],
                        "id": "cUdLtk1Ahm"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "未来增长潜力"
                                    }
                                ],
                                "id": "0CVphgBEZr"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉在全球市场扩张中具有巨大潜力，特别是在新兴市场如印度和东南亚。此外，FSD（完全自动驾驶）技术和电池技术的突破将为其带来新的收入来源。"
                                    }
                                ],
                                "id": "MXsd1dQAI-"
                            }
                        ],
                        "id": "6ffe1enX75"
                    }
                ],
                "id": "x1EUFy0C3R"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Tesla challenges and future prospects",
            "url": "https://n.sinaimg.cn/spider20250610/598/w955h443/20250610/d5d4-b0eb5848953ded18fbc44aefb452923d.png",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "kp8wqwwK5wj_aZIg8OsC4",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉的市场扩张与全球化战略"
                    }
                ],
                "id": "g-QwuNImsJ"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "全球市场扩张"
                                    }
                                ],
                                "id": "UEpuyIdugA"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉正在推进本地化生产计划，例如在中国和德国建设超级工厂，以降低运输成本并提高市场响应速度。"
                                    }
                                ],
                                "id": "Xb3pXGDIaz"
                            }
                        ],
                        "id": "lBazhK7w1m"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "新兴市场机会"
                                    }
                                ],
                                "id": "galszc55Mg"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "印度、东南亚等新兴市场成为特斯拉的重点扩展方向，但需克服政策和基础设施限制。"
                                    }
                                ],
                                "id": "wXw0AdR7yl"
                            }
                        ],
                        "id": "yyBao4j3YB"
                    }
                ],
                "id": "b9J1xaY5X9"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Tesla global expansion strategy",
            "url": "https://n.sinaimg.cn/spider20250610/598/w955h443/20250610/d5d4-b0eb5848953ded18fbc44aefb452923d.png",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "7voQ5e4hggtoaSek_YGGw",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉的全球化战略与本地化生产"
                    }
                ],
                "id": "Lux82bMEPV"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "全球市场扩张"
                                    }
                                ],
                                "id": "P0fspVVGr0"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉正在推进本地化生产计划，例如在中国和德国建设超级工厂，以降低运输成本并提高市场响应速度。"
                                    }
                                ],
                                "id": "Jpxrqh_qGG"
                            }
                        ],
                        "id": "mwa91YKrbu"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "新兴市场机会"
                                    }
                                ],
                                "id": "80vK3tTymo"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "印度、东南亚等新兴市场成为特斯拉的重点扩展方向，但需克服政策和基础设施限制。"
                                    }
                                ],
                                "id": "8tSM2IFQOL"
                            }
                        ],
                        "id": "z7GH6KrCKs"
                    }
                ],
                "id": "c463mxyNyi"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Tesla global expansion strategy",
            "url": "https://n.sinaimg.cn/spider20250610/598/w955h443/20250610/d5d4-b0eb5848953ded18fbc44aefb452923d.png",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "dsTWMJpHAUmdLQ2bQAwVx",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉的全球化战略与本地化生产"
                    }
                ],
                "id": "TmVVrZawhs"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "全球市场扩张"
                                    }
                                ],
                                "id": "B5Uphjvhyw"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉正在推进本地化生产计划，例如在中国和德国建设超级工厂，以降低运输成本并提高市场响应速度。"
                                    }
                                ],
                                "id": "g_sd3C2Txv"
                            }
                        ],
                        "id": "QsUaSuQiVI"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "新兴市场机会"
                                    }
                                ],
                                "id": "PQkyvQuyQk"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "印度、东南亚等新兴市场成为特斯拉的重点扩展方向，但需克服政策和基础设施限制。"
                                    }
                                ],
                                "id": "EbHbBGaBzS"
                            }
                        ],
                        "id": "UtFU5zml4z"
                    }
                ],
                "id": "n4NVulKJzn"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Tesla global expansion strategy",
            "url": "https://cdn.pixabay.com/photo/2024/12/18/15/02/old-9275581_640.jpg",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "zfWnbseSqZveQtxH5KHTG",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉的全球市场扩张与本地化生产"
                    }
                ],
                "id": "8OTGC3IPFd"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "全球市场扩张"
                                    }
                                ],
                                "id": "fJ_qZs3b4-"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉正在推进本地化生产计划，例如在中国和德国建设超级工厂，以降低运输成本并提高市场响应速度。"
                                    }
                                ],
                                "id": "iTMHgRX0Ur"
                            }
                        ],
                        "id": "5zbw3jLmCt"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "新兴市场机会"
                                    }
                                ],
                                "id": "XMbrJ7khQy"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "印度、东南亚等新兴市场成为特斯拉的重点扩展方向，但需克服政策和基础设施限制。"
                                    }
                                ],
                                "id": "lWuTdDTpMr"
                            }
                        ],
                        "id": "--E-W3gMGT"
                    }
                ],
                "id": "E8rt3Dcr28"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Tesla global expansion strategy",
            "url": "https://n.sinaimg.cn/spider20250610/598/w955h443/20250610/d5d4-b0eb5848953ded18fbc44aefb452923d.png",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    },
    {
        "id": "TEqcpxtIbejZAEY47cWv0",
        "content": [
            {
                "type": "h1",
                "children": [
                    {
                        "text": "特斯拉的可持续发展与环境影响"
                    }
                ],
                "id": "4zF69jZYen"
            },
            {
                "type": "bullets",
                "children": [
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "减少碳足迹"
                                    }
                                ],
                                "id": "R8ChCJYkVK"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉通过制造电动汽车减少了传统燃油车的碳排放，尤其是在电力来源清洁的地区，其全生命周期碳排放显著低于燃油车。"
                                    }
                                ],
                                "id": "DRqPQzvhrc"
                            }
                        ],
                        "id": "ey6nZ58uu7"
                    },
                    {
                        "type": "bullet",
                        "children": [
                            {
                                "type": "h3",
                                "children": [
                                    {
                                        "text": "推动可再生能源"
                                    }
                                ],
                                "id": "AzBGurXru0"
                            },
                            {
                                "type": "p",
                                "children": [
                                    {
                                        "text": "特斯拉开发了太阳能产品和储能系统，鼓励用户采用清洁能源。公司致力于建设全球范围内的超级充电站，并逐步转向使用可再生能源供电。"
                                    }
                                ],
                                "id": "-wcBBI4GqI"
                            }
                        ],
                        "id": "eYUyIUhhsB"
                    }
                ],
                "id": "dlyHYheu0A"
            }
        ],
        "alignment": "center",
        "rootImage": {
            "alt": "Battery degradation curve",
            "url": "https://n.sinaimg.cn/spider20250610/598/w955h443/20250610/d5d4-b0eb5848953ded18fbc44aefb452923d.png",
            "query": "",
            "background": False
        },
        "layoutType": "vertical"
    }
]


def test_root_endpoint():
    """测试根路径 / 接口"""
    print("\n--- Testing GET / ---")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
        assert response.status_code == 200
        assert "Welcome" in response.json().get("message", "")
        print("GET / passed.")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to FastAPI server at {BASE_URL}. Is it running?")
        print("Please ensure your FastAPI server is running with: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        exit(1)  # Exit if server is not running
    except Exception as e:
        print(f"Error testing GET /: {e}")
        print("GET / failed.")


def test_generate_ppt_success():
    """测试 /generate-ppt 接口的成功情况"""
    print("\n--- Testing POST /generate-ppt (Success) ---")

    try:
        # 添加一个唯一ID到标题，以确保每次生成的文件名不同，避免缓存问题
        # 实际生产中可能通过时间戳或UUID来管理文件名
        unique_id = int(time.time())
        original_title_block = front_data["sections"][0]["content"][0]["children"][0]["text"]
        new_title = f"{original_title_block} - Test_{unique_id}"
        front_data["sections"][0]["content"][0]["children"][0]["text"] = new_title

        response = requests.post(f"{BASE_URL}/generate-ppt", json=front_data, timeout=120)  # 增加超时时间
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

        print(f"Status Code: {response.status_code}")
        response_json = response.json()
        print(f"Response Body: {response_json}")

        assert response.status_code == 200
        assert "ppt_url" in response_json
        assert response_json["ppt_url"].endswith(".pptx")

        ppt_local_path = response_json["ppt_url"]
        print(f"Generated PPT URL: {ppt_local_path}")

        # 尝试下载PPT文件
        full_ppt_url = f"{BASE_URL}{ppt_local_path}"
        print(f"Attempting to download PPT from: {full_ppt_url}")

        ppt_response = requests.get(full_ppt_url, stream=True, timeout=120)
        ppt_response.raise_for_status()

        # 从URL中提取文件名
        filename = os.path.basename(ppt_local_path)
        download_path = os.path.join(OUTPUT_TEST_DIR, filename)

        with open(download_path, 'wb') as f:
            for chunk in ppt_response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"PPT successfully downloaded to: {download_path}")
        print("POST /generate-ppt (Success) passed.")

    except requests.exceptions.Timeout:
        print("Error: Request timed out. PPT generation might be taking too long or server is slow.")
        print("POST /generate-ppt (Success) failed.")
    except requests.exceptions.RequestException as e:
        print(f"Error testing POST /generate-ppt (Success): {e}")
        print(f"Response content: {response.text if 'response' in locals() else 'No response'}")
        print("POST /generate-ppt (Success) failed.")
    except AssertionError as e:
        print(f"Assertion failed: {e}")
        print("POST /generate-ppt (Success) failed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("POST /generate-ppt (Success) failed.")


def test_generate_ppt_invalid_input():
    """测试 /generate-ppt 接口的无效输入情况"""
    print("\n--- Testing POST /generate-ppt (Invalid Input) ---")
    invalid_data = {"wrong_key": "some_value"}  # 缺少 'sections' 键

    try:
        response = requests.post(f"{BASE_URL}/generate-ppt", json=invalid_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")

        assert response.status_code == 422  # FastAPI Pydantic验证失败通常返回422
        assert "detail" in response.json()
        print("POST /generate-ppt (Invalid Input) passed.")
    except Exception as e:
        print(f"Error testing POST /generate-ppt (Invalid Input): {e}")
        print("POST /generate-ppt (Invalid Input) failed.")


if __name__ == "__main__":
    print("Starting FastAPI API tests...")

    # 运行各项测试
    test_root_endpoint()

    # 等待几秒，确保服务器启动并准备好处理后续请求
    time.sleep(2)

    test_generate_ppt_success()
    test_generate_ppt_invalid_input()

    print("\nAll tests finished.")
    print(f"Generated PPTs (if successful) are saved in the '{OUTPUT_TEST_DIR}' directory.")