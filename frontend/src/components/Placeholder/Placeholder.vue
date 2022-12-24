<template>
    <div class="custom-placeholder">
        <canvas :id="placeholderId"></canvas>
    </div>
</template>

<script>
import { fabric } from 'fabric';
export default {
    name: 'Placeholder',
    props: {
        canvasWidth: {
            type: [String, Number],
            required: true
        },
        canvasHeight: {
            type: [String, Number],
            required: true
        },
        placeholderId: {
            type: String,
            default: 'c',
            required: false
        }
    },
    data() {
        return {
            canvas: null,
            width: null,
            height: null,
            color: '#000000',
            strokeWidth: 7,
            fontSize: 32,
            croppedImage: false,
        }

    },
    mounted() {
        this.canvas = new fabric.Canvas(this.placeholderId);
        this.canvas.setDimensions({ width: this.canvasWidth, height: this.canvasHeight });
        this.canvas.backgroundColor = "#fff";
    },
    methods: {
        getBackgroundImage() {
            return this.canvas.backgroundImage.toDataURL('image/jpeg', 1)
        },
        setBackgroundImageFromFile(file) {
            let img = new Image();
            let url = URL.createObjectURL(file);
            img.src = url;
            let inst = this;
            img.onload = function () {
                let image = new fabric.Image(img);
                image.scaleToWidth(inst.canvasWidth);
                image.scaleToHeight(inst.canvasHeight);
                inst.canvas.setBackgroundImage(image, inst.canvas.renderAll.bind(inst.canvas));
                inst.canvas.renderAll();
            }
        },
        setBackgroundImage(imageUrl, backgroundColor = "#fff") {
            let img = new Image();
            this.toDataUrl(imageUrl, (dataUri) => {
                img.src = dataUri;
                let inst = this;
                img.onload = function () {
                    let image = new fabric.Image(img);
                    image.scaleToWidth(inst.canvasWidth);
                    image.scaleToHeight(inst.canvasHeight);
                    inst.canvas.setBackgroundImage(image, inst.canvas.renderAll.bind(inst.canvas));
                    inst.canvas.renderAll();
                }

            });
        },
        toDataUrl(url, callback) {
            let xhr = new XMLHttpRequest();
            xhr.onload = function () {
                let reader = new FileReader();
                reader.onloadend = () => {
                    callback(reader.result);
                };
                reader.readAsDataURL(xhr.response);
            };
            xhr.open('GET', url);
            xhr.responseType = 'blob';
            xhr.send();
        },
        saveImage() {
            this.cancelCroppingImage();
            return this.canvas.toDataURL('image/jpeg', 1);
        },
        uploadImage(e) {
            this.cancelCroppingImage();
            let inst = this;
            let reader = new FileReader();
            reader.onload = function (event) {
                let imgObj = new Image();
                imgObj.src = event.target.result;
                imgObj.onload = function () {
                    let image = new fabric.Image(imgObj);
                    if (inst.canvas.width <= image.width || inst.canvas.height <= image.height) {
                        let canvasAspect = inst.canvas.width / inst.canvas.height;
                        let imgAspect = image.width / image.height;
                        let top, left, scaleFactor;
                        if (canvasAspect >= imgAspect) {
                            scaleFactor = inst.canvas.height / image.height
                            top = 0;
                            left = -((image.width * scaleFactor) - inst.canvas.width) / 2;
                        } else {
                            scaleFactor = inst.canvas.width / image.width;
                            left = 0;
                            top = -((image.height * scaleFactor) - inst.canvas.height) / 2;
                        }
                        inst.canvas.setBackgroundImage(image, inst.canvas.renderAll.bind(inst.canvas), {
                            top: top,
                            left: left,
                            scaleX: scaleFactor,
                            scaleY: scaleFactor
                        });
                        inst.canvas.renderAll();
                    } else {
                        let center = inst.canvas.getCenter();
                        inst.canvas.setBackgroundImage(image, inst.canvas.renderAll.bind(inst.canvas), {
                            top: center.top,
                            left: center.left,
                            originX: 'center',
                            originY: 'center'
                        });
                        let canvasProperties = { width: inst.canvas.width, height: inst.canvas.height };
                        inst.canvas.renderAll();
                    }
                }
            };
            reader.readAsDataURL(e.target.files[0]);
        },
    }

}
</script>
<style>
.upper-canvas {
    z-index: 1;
}
</style>
