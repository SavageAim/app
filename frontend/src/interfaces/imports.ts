export interface ImportError {
  message: string
}

export interface XIVGearSheetSelection {
  name: string
  index: number
}

export interface ExternalBISGearImportResponse {
  job_id: string
  job_name: string
  mainhand: number
  offhand: number
  head: number
  body: number
  hands: number
  legs: number
  feet: number
  earrings: number
  necklace: number
  bracelet: number
  left_ring: number
  right_ring: number

  name: string
  min_il: number
  max_il: number
}

export interface LodestoneImportResponse {
  job_id: string
  mainhand: number
  offhand: number
  head: number
  body: number
  hands: number
  legs: number
  feet: number
  earrings: number
  necklace: number
  bracelet: number
  left_ring: number
  right_ring: number

  min_il: number
  max_il: number
}
