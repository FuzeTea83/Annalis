export type View = 'overview' | 'explorer' | 'upload' | 'account'

export interface NavItem {
  id: View
  label: string
  icon: string
}

