<template>
    <div class='segmenter'>
        <div class='label' id='input-label'>Input</div>
        <Placeholder :canvasWidth="canvas_width" :canvasHeight="canvas_height" ref='placeholder' id='input-image'
            class='image' />

        <div id='load-buttons' class='load-buttons'>

            <div class='button' id='load-image'>
                <!--default html file upload button-->
                <input type="file" id="inp-btn-upload" @change="load_image_from_file" hidden />
                <label for="inp-btn-upload">Load</label>
            </div>

            <div class='button' id='random-image' @click="load_random_image">Random</div>
        </div>

        <div class='nn' id='nn1'>
            <div class='layer' id='layer1' style='height: 256px;' />
            <div class='layer' id='layer1' style='height: 256px;' />
            <div class='layer' id='layer1' style='height: 190px;' />
            <div class='layer' id='layer1' style='height: 190px;' />
            <div class='layer' id='layer1' style='height: 140px;' />
            <div class='layer' id='layer1' style='height: 140px;' />
            <div class='layer' id='layer1' style='height: 100px;' />
            <div class='layer' id='layer1' style='height: 100px;' />
            <div class='layer' id='layer1' style='height: 140px;' />
            <div class='layer' id='layer1' style='height: 140px;' />
            <div class='layer' id='layer1' style='height: 190px;' />
            <div class='layer' id='layer1' style='height: 190px;' />
            <div class='layer' id='layer1' style='height: 256px;' />
            <div class='layer' id='layer1' style='height: 256px;' />
        </div>

        <div class='label' id='output-label'>Result</div>
        <div class='image' id='output-image'></div>
        <div class='button' id='compute' @click='run_model'>Compute</div>

    </div>
</template>

<script>
import Placeholder from '@/components/Placeholder/Placeholder.vue'
import axios from 'axios'

export default {
    name: 'Segmenter',
    components: {
        Placeholder,
    },
    data: () => {
        return {
            canvas_width: '320',
            canvas_height: '320',

            /* server */
            server_host: 'http://backend:1337',
        }
    },
    methods: {
        image2base64(url) {
            var xhr = new XMLHttpRequest()
            /* xhr.responseType = 'blob' */
            xhr.open('GET', url, false)
            xhr.send()
            print(xhr.response)

            var reader = new FileReader()
            return reader.readAsDataURL(xhr.response)
        },
        load_random_image() {
            this.$refs.placeholder.setBackgroundImage('/api/random_image')
        },
        load_image_from_file(event) {
            this.$refs.placeholder.setBackgroundImageFromFile(event.target.files[0])
        },
        run_model() {
            console.log('run_model')
            let bg_image = this.$refs.placeholder.getBackgroundImage()

            axios.post('/api/run_model', {
                'image': bg_image,
            }).then(function (response) {
                let image_data = response.data
                let elem = document.getElementById('output-image')
                elem.style.backgroundImage = "url(" + image_data + ")"
            })
        },
    },
    mounted() {
        this.set_active_tool(this.active_tool)
    }
}
</script>

<style lang='scss' scoped>
.segmenter {
    display: grid;
    justify-content: center;
    row-gap: 20px;

    grid-template:
        [row1-start] "input-label   .     output-label"[row1-end] [row2-start] "input-image   nn    output-image"[row2-end] [row3-start] "choose-random tools compute     "[row3-end] / 340px 470px 340px;

    .image {
        justify-self: center;
        width: 320px;
        height: 320px;
        border: 12px solid #eee;

        border-radius: 5px;
        background-color: #fff;
    }

    .load-buttons {
        justify-self: center;

        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: flex-start;

        #random-image {
            width: 90px;
        }

        #load-image {
            width: 90px;
            margin-right: 20px;
        }
    }

    .label {
        justify-self: center;
        font-family: sans-serif;
        font-size: 1.5rem;
        color: $TEXTCOLOR;
    }

    .button {
        justify-self: center;
        font-size: 1rem;
        font-family: sans-serif;
        color: $TEXTCOLOR;
        user-select: none;

        width: auto;
        height: 30px;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;

        /* margin-top: 20px; */
        padding: 5px 16px;
        border-radius: 50px;
        background: #d1d1d1;
        box-shadow: 6px 6px 12px #b2b2b2,
            -6px -6px 12px #f0f0f0;

        &:active {
            border-radius: 50px;
            left: -20px;
            background: #e0e0e0;
            box-shadow: inset 6px 6px 11px #bebebe,
                inset -6px -6px 11px #ffffff;
        }


    }

    .nn {
        justify-self: center;
        align-self: center;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;

        .layer {
            width: 20px;
            border-radius: 20px;
            margin: 0 5px;

            border-radius: 50px;
            background-color: #d1d1d1;
            box-shadow: 4px 4px 9px #b2b2b2,
                -4px -4px 9px #f0f0f0;

            &:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        }
    }

    #nn1 {
        grid-area: nn;
    }

    #input-image {
        grid-area: input-image;
    }

    #input-label {
        grid-area: input-label;
    }

    #output-label {
        grid-area: output-label;
    }

    #output-image {
        grid-area: output-image;
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
    }

    #load-buttons {
        grid-area: choose-random;
    }

    #compute {
        grid-area: compute;
        width: 90px;
    }

    #tools-panel {
        grid-area: tools;
    }
}
</style>
