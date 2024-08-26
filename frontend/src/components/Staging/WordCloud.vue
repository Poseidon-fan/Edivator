<template>
    <div ref="wordCloudContainer" class="word-cloud"></div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue'
import * as echarts from 'echarts'
import 'echarts-wordcloud'

const props = defineProps({
    words: {
        type: Array,
        required: true,
    },
})

const wordCloudContainer = ref(null)
let chart = null

const drawWordCloud = () => {
    if (chart) {
        chart.dispose()
    }
    chart = echarts.init(wordCloudContainer.value)
    const option = {
        series: [
            {
                type: 'wordCloud',
                shape: 'circle',
                left: 'center',
                top: 'center',
                width: '500px',
                height: '500px',
                right: null,
                bottom: null,
                sizeRange: [20, 60],
                rotationRange: [-90, 90],
                rotationStep: 45,
                gridSize: 15,
                drawOutOfBound: false,
                textStyle: {
                    normal: {
                        color: function () {
                            return (
                                'rgb(' +
                                [
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160),
                                    Math.round(Math.random() * 160),
                                ].join(',') +
                                ')'
                            )
                        },
                    },
                    emphasis: {
                        shadowBlur: 10,
                        shadowColor: '#333',
                    },
                },
                data: props.words.map(([name, value]) => ({ name, value })),
            },
        ],
    }
    chart.setOption(option)
}

onMounted(() => {
    drawWordCloud()
})

watch(
    () => props.words,
    () => {
        drawWordCloud()
    }
)
</script>

<style scoped>
.word-cloud {
    width: 500px;
    height: 500px;
}
</style>
