export type CropMode = 'avatar' | 'image'

export interface CropOptions {
  mode: CropMode
  aspectRatio: number // e.g. 1 or 4/3
  cropWidth: number
  cropHeight: number
}

