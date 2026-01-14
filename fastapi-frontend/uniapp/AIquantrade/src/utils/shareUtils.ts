//封装一个generateShareQRCode 函数，传入2个参数，
// 参数是生成二维码的链接，和背景图
// 链接的二维码放置在背景图的中间，背景图的为手机竖屏的比例，高度不大于1280像素，生成后的图片保持到相册中

import { createCanvas, loadImage } from 'canvas'
// Removed unused import for saveImageToPhotosAlbum
export async function generateShareQRCode(url: string, backgroundUrl: string): Promise<string> {
    const { screenWidth, screenHeight } = uni.getSystemInfoSync()
    const canvasWidth = screenWidth
    const canvasHeight = Math.min(screenHeight, 1280)

    const canvas = createCanvas(canvasWidth, canvasHeight)
    const ctx = canvas.getContext('2d')

    // 加载背景图
    const backgroundImage = await loadImage(backgroundUrl)
    ctx.drawImage(backgroundImage, 0, 0, canvasWidth, canvasHeight)

    // 加载二维码图片
    const qrImage = await loadImage(url)
    
    // 绘制二维码图片在画布中心
    const qrSize = Math.min(canvasWidth * 0.8, canvasHeight * 0.8) // 设置二维码大小为画布的80%
    const x = (canvasWidth - qrSize) / 2
    const y = (canvasHeight - qrSize) / 2

    ctx.drawImage(qrImage, x, y, qrSize, qrSize)

    return canvas.toDataURL('image/png')
}