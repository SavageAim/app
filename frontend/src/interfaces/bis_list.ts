import Gear from './gear'
import Job from './job'

export default interface BISList {
  bis_body: Gear
  bis_bracelet: Gear
  bis_earrings: Gear
  bis_feet: Gear
  bis_hands: Gear
  bis_head: Gear
  bis_left_ring: Gear
  bis_legs: Gear
  bis_mainhand: Gear
  bis_necklace: Gear
  bis_offhand: Gear
  bis_right_ring: Gear

  current_body: Gear
  current_bracelet: Gear
  current_earrings: Gear
  current_feet: Gear
  current_hands: Gear
  current_head: Gear
  current_left_ring: Gear
  current_legs: Gear
  current_mainhand: Gear
  current_necklace: Gear
  current_offhand: Gear
  current_right_ring: Gear
  external_link: string | null
  id: number
  item_level: number
  job: Job
}
