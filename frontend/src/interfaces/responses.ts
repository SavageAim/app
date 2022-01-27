// Interface defining the errors response from the BISList endpoints
export interface BISListErrors {
  id?: string[],
  job?: string[],

  bis_body?: string[],
  bis_bracelet?: string[],
  bis_earrings?: string[],
  bis_feet?: string[],
  bis_hands?: string[],
  bis_head?: string[],
  bis_left_ring?: string[],
  bis_legs?: string[],
  bis_mainhand?: string[],
  bis_necklace?: string[],
  bis_offhand?: string[],
  bis_right_ring?: string[],
  current_body?: string[],
  current_bracelet?: string[],
  current_earrings?: string[],
  current_feet?: string[],
  current_hands?: string[],
  current_head?: string[],
  current_left_ring?: string[],
  current_legs?: string[],
  current_mainhand?: string[],
  current_necklace?: string[],
  current_offhand?: string[],
  current_right_ring?: string[],
  external_link?: string[],
}

// All create responses will return just the ID of the new item.
export interface CreateResponse {
  id: number
}

// Interface defining the potential error responses that can come from the Character.create method
export interface CharacterCreateErrors {
  lodestone_id: string[]
}

// Interface for defining errors that can be returned from Loot create
export interface LootCreateErrors {
  greed?: string[]
  item?: string[]
  member_id?: string[]
  obtained?: string[]
}

// Interface for defining errors that can be returned from Loot create with BIS
export interface LootBISCreateErrors {
  greed?: string[]
  greed_bis_id?: string[]
  item?: string[]
  member_id?: string[]
}

// Settings errors response
export interface SettingsErrors {
  theme?: string[]
}

// Team create response will return a string id since it uses uuid
export interface TeamCreateResponse {
  id: string
}

// Interface defining possible errors with the Team Create View
export interface TeamCreateErrors {
  bis_list_id?: string[]
  character_id?: string[]
  name?: string[]
  tier_id?: string[]
}

// Interface defining possible errors with the Team Member update view, or Team Join view, or any view that uses
// TeamMemberForm
export interface TeamMemberUpdateErrors {
  bis_list_id?: string[]
  character_id?: string[]
}

// Interface defining possible errors with the Team Update view
export interface TeamUpdateErrors {
  name?: string[]
  tier_id?: string[]
  team_lead?: string[]
}
