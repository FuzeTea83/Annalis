export interface DocumentItem {
  id: string
  title: string
  description?: string
  createdAt: Date
  contentType: string
  format: string
  subject: string
  sector: string
  sector_year: number
  school_year: number
  session?: 1 | 2
  author: string
  size: number
  viewedAt?: Date
}
