<template>
    <div ref="chart" style="width: 100%; height: 400px"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chart = ref(null)

onMounted(() => {
    const myChart = echarts.init(chart.value)
    const option = {
        title: {
            text: 'XX 指数',
            left: 'left',
        },
        tooltip: {},
        legend: {
            data: ['数据A', '数据B', '数据C'],
            bottom: 0,
        },
        radar: {
            // shape: 'circle',
            indicator: [
                { name: '引用', max: 5 },
                { name: '热度', max: 5 },
                { name: '贡献', max: 5 },
                { name: '产量', max: 5 },
                { name: '口碑', max: 5 },
            ],
        },
        series: [
            {
                name: '预算 vs 开销',
                type: 'radar',
                data: [
                    {
                        value: [5, 3, 4, 2, 4],
                        name: '数据A',
                    },
                    {
                        value: [2, 3, 4, 3, 4],
                        name: '数据B',
                    },
                    {
                        value: [3, 4, 3, 5, 2],
                        name: '数据C',
                    },
                ],
            },
        ],
    }
    myChart.setOption(option)
})
</script>

<style scoped>
/* 添加你的样式 */
</style>
