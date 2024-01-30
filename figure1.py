import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable

# 读取Excel文件
data = pd.read_excel("./Texas.xlsx")

# 设置最大GDP值为50000
max_gdp_value = 15

# 根据Rate排序
data.sort_values(by="Rate_HasCooling", ascending=True, inplace=True)

rate_hascooling = np.array(data["Rate_HasCooling"])
population_percentages = np.array(data["Population Percentage"])
gdp2021 = np.array(data["GDP3"])
counties = np.array(data["County"])  # 添加县的名称

# 要标注的县名
highlighted_counties = [
     "McMullen",    "Webb",
    #"Duval","Live Oak",    "Jim Wells",#差的方块，南部
    # "Donley", "Deaf Smith",
    "Carson",
   # "Moore", "Hutchinson",
    "Roberts",#差的方块，北部
    "Denton",
    "Bexar",  # d
    "Travis", "Williamson ",  # b
    "Harris", "Montgomery",  # a
    "Nueces", "San Patricio",  # e
    "Hidalgo",  # f
    "Cameron",  # f-2
    "Dallas", "Denton", "Collin",  # c
    "El Paso",
    "McLennan", "Smith",   # 小城市
    "Reeves","Midland",
    "Harris",
    "Ector", "Potter", "Harrison"

    "Tarrant",  # c-2
]

# 需要添加指引线的县名
counties_with_lines = [ "San Patricio", "Montgomery","Ector", "Cameron","Potter",
                       "McMullen", "Webb", "Denton","Reeves","Midland",
                       #"Duval", "Live Oak","Denton"
                       "Jim Wells",  # 差的方块，南部
                      # "Donley", "Deaf Smith",
                        "Roberts",  # 差的方块，北部
                       ]  # 您可以根据需要在这里添加或删除县名

# 创建颜色映射
norm = Normalize(0, max_gdp_value)
cmap = LinearSegmentedColormap.from_list("custom_cmap", ["#cfe2f1", "#1764aa"], N=256)
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# 调整表格宽度和高度
plt.figure(figsize=(13, 6))

current_x = 0
for i in range(len(population_percentages)):
    color = "#0b3d91" if gdp2021[i] > max_gdp_value else cmap(norm(gdp2021[i]))
    plt.bar(current_x + population_percentages[i] / 2, rate_hascooling[i], width=population_percentages[i],
            align="center", color=color)

    if counties[i] in highlighted_counties:
        plt.scatter(current_x + population_percentages[i] / 2, rate_hascooling[i], marker="o", color="k", s=5)

        # 判断是否需要添加指引线
        if counties[i] in counties_with_lines:
            # 对每个县设置不同的 xytext_position
            if counties[i] == "Jefferson":
                xytext_position = (current_x - 4 * population_percentages[i], rate_hascooling[i] + 0.01)
            elif counties[i] == "Montgomery":
                xytext_position = (current_x - 1 * population_percentages[i], rate_hascooling[i] + 0.03)
            elif counties[i] == "Denton":
                xytext_position = (current_x - 0.03 * population_percentages[i], rate_hascooling[i] + 0.02)
            elif counties[i] == "McMullen":
                xytext_position = (current_x - 49 * population_percentages[i], rate_hascooling[i] + 0.01)
            elif counties[i] == "San Patricio":
                xytext_position = (current_x - 25 * population_percentages[i], rate_hascooling[i] + 0.15)
            elif counties[i] == "Ector" or counties[i] == "Midland" or counties[i] == "Reeves":
                xytext_position = (current_x - 9 * population_percentages[i], rate_hascooling[i] + 0.02)
            elif counties[i] == "Cameron":
                xytext_position = (current_x - 5 * population_percentages[i], rate_hascooling[i] + 0.05)
            elif counties[i] == "Webb":
                xytext_position = (current_x - 5 * population_percentages[i], rate_hascooling[i] + 0.06)
            else:
                xytext_position = (current_x - 8 * population_percentages[i], rate_hascooling[i] + 0.06)
            plt.annotate(
                counties[i],
                xy=(current_x + population_percentages[i] / 2, rate_hascooling[i]),
                xytext=xytext_position,
                ha="center",
                arrowprops=dict(facecolor='black', arrowstyle="-"),
                fontsize=8
            )
        else:
            plt.text(
                current_x + population_percentages[i] / 2,
                rate_hascooling[i] + 0.005,
                counties[i],
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=0,
            )

    current_x += population_percentages[i]

# 计算hascooling的中位数
median_hascooling = np.median(rate_hascooling)

# 在hascooling的中位数位置添加一条线
plt.axhline(y=median_hascooling, color='orangered', linestyle='--', lw=1, label='The Median Level of RCI prevalence')  # 使用绿色实线表示中位数

# 添加两条虚线
plt.axhline(y=0.6, color='grey', linestyle='--', lw=1)
plt.axhline(y=0.9, color='grey', linestyle='--',lw=1 )

# 请注意，我们只是为了图例需要添加这个散点，它并不代表实际数据
plt.scatter([], [], marker="o", color="k", s=5, label='Counties in Texas')

# 显示图例
legend = plt.legend(frameon = 1, loc='upper left', fontsize='small')
frame = legend.get_frame()
frame.set_color('white')


# # 设置y轴的刻度间隔为0.1
# plt.yticks(np.arange(0, max(rate_hascooling) + 0.1, 0.1))
#
# # 添加白色的水平格网线，间隔为0.1
# plt.grid(axis='y', linestyle='-', color='white', linewidth=0.7, which='both', alpha=0.7)



cb = plt.colorbar(sm, ax=plt.gca(), pad=0.02, orientation="vertical", aspect=40, shrink=0.6)
cb.set_label("GDP per capita (USD*10^4)")

plt.xlabel("Proportion of the population across various counties in Texas")
plt.xticks([])
plt.ylabel("Prevalence of RCI Across Counties")

plt.tight_layout()
plt.show()
