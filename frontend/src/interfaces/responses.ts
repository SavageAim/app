// Interface defining the errors response from the BISList endpoints
export interface BISListErrors {
  id?: string[],
  job_id?: string[],

  bis_body_id?: string[],
  bis_bracelet_id?: string[],
  bis_earrings_id?: string[],
  bis_feet_id?: string[],
  bis_hands_id?: string[],
  bis_head_id?: string[],
  bis_left_ring_id?: string[],
  bis_legs_id?: string[],
  bis_mainhand_id?: string[],
  bis_necklace_id?: string[],
  bis_offhand_id?: string[],
  bis_right_ring_id?: string[],
  current_body_id?: string[],
  current_bracelet_id?: string[],
  current_earrings_id?: string[],
  current_feet_id?: string[],
  current_hands_id?: string[],
  current_head_id?: string[],
  current_left_ring_id?: string[],
  current_legs_id?: string[],
  current_mainhand_id?: string[],
  current_necklace_id?: string[],
  current_offhand_id?: string[],
  current_right_ring_id?: string[],
  external_link?: string[],
}

export interface BISListDeleteReadResponse {
  id: string
  member: number
  name: string
}

// All create responses will return just the ID of the new item.
export interface CreateResponse {
  id: number
}

// Interface defining the potential error responses that can come from the Character.create method
export interface CharacterCreateErrors {
  lodestone_id: string[]
}

// Information about deleting Characters
export interface CharacterDeleteReadResponse {
  lead: boolean
  members: number
  name: string
}

// Errors that can arise from updating characters
export interface CharacterUpdateErrors {
  alias?: string[]
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
