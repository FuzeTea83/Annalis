export interface DocumentItem {
  title: string
  description?: string
  createdAt: Date
  contentType: string
  course: string
  sector: string
  sector_year: number
  school_year: number
  session: 0 | 1 | 2
  owner: string
  owner_initials: string
  date: string
  tone: string
}

