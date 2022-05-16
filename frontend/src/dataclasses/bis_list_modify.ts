// Slight variation on bis_list that is used for sending create / update requests
// Done as a class instead of an interface to allow for functions and such
import BISList from '@/interfaces/bis_list'
import { ImportResponse } from '@/interfaces/imports'

export default class BISListModify {
  public id = -1
  public job_id = 'PLD'

  public bis_body_id = -1
  public bis_bracelet_id = -1
  public bis_earrings_id = -1
  public bis_feet_id = -1
  public bis_hands_id = -1
  public bis_head_id = -1
  public bis_left_ring_id = -1
  public bis_legs_id = -1
  public bis_mainhand_id = -1
  public bis_necklace_id = -1
  public bis_offhand_id = -1
  public bis_right_ring_id = -1
  public current_body_id = -1
  public current_bracelet_id = -1
  public current_earrings_id = -1
  public current_feet_id = -1
  public current_hands_id = -1
  public current_head_id = -1
  public current_left_ring_id = -1
  public current_legs_id = -1
  public current_mainhand_id = -1
  public current_necklace_id = -1
  public current_offhand_id = -1
  public current_right_ring_id = -1
  public external_link: string | null = null
  public name = ''
  public display_name = ''

  static buildEditVersion(responseList: BISList): BISListModify {
    // Create an instance of this dataclass from an object with the BISList interface
    const newList = new BISListModify()
    newList.id = responseList.id
    newList.job_id = responseList.job.id

    newList.bis_body_id = responseList.bis_body.id
    newList.bis_bracelet_id = responseList.bis_bracelet.id
    newList.bis_earrings_id = responseList.bis_earrings.id
    newList.bis_feet_id = responseList.bis_feet.id
    newList.bis_hands_id = responseList.bis_hands.id
    newList.bis_head_id = responseList.bis_head.id
    newList.bis_left_ring_id = responseList.bis_left_ring.id
    newList.bis_legs_id = responseList.bis_legs.id
    newList.bis_mainhand_id = responseList.bis_mainhand.id
    newList.bis_necklace_id = responseList.bis_necklace.id
    newList.bis_offhand_id = responseList.bis_offhand.id
    newList.bis_right_ring_id = responseList.bis_right_ring.id

    newList.current_body_id = responseList.current_body.id
    newList.current_bracelet_id = responseList.current_bracelet.id
    newList.current_earrings_id = responseList.current_earrings.id
    newList.current_feet_id = responseList.current_feet.id
    newList.current_hands_id = responseList.current_hands.id
    newList.current_head_id = responseList.current_head.id
    newList.current_left_ring_id = responseList.current_left_ring.id
    newList.current_legs_id = responseList.current_legs.id
    newList.current_mainhand_id = responseList.current_mainhand.id
    newList.current_necklace_id = responseList.current_necklace.id
    newList.current_offhand_id = responseList.current_offhand.id
    newList.current_right_ring_id = responseList.current_right_ring.id
    newList.external_link = responseList.external_link

    newList.name = responseList.name
    newList.display_name = responseList.display_name

    return newList
  }

  importBIS(data: ImportResponse): void {
    this.job_id = data.job_id
    this.bis_mainhand_id = data.mainhand
    this.bis_offhand_id = data.offhand
    this.bis_head_id = data.head
    this.bis_body_id = data.body
    this.bis_hands_id = data.hands
    this.bis_legs_id = data.legs
    this.bis_feet_id = data.feet
    this.bis_earrings_id = data.earrings
    this.bis_necklace_id = data.necklace
    this.bis_bracelet_id = data.bracelet
    this.bis_left_ring_id = data.left_ring
    this.bis_right_ring_id = data.right_ring
  }

  importCurrent(data: BISList): void {
    this.current_body_id = data.current_body.id
    this.current_bracelet_id = data.current_bracelet.id
    this.current_earrings_id = data.current_earrings.id
    this.current_feet_id = data.current_feet.id
    this.current_hands_id = data.current_hands.id
    this.current_head_id = data.current_head.id
    this.current_left_ring_id = data.current_left_ring.id
    this.current_legs_id = data.current_legs.id
    this.current_mainhand_id = data.current_mainhand.id
    this.current_necklace_id = data.current_necklace.id
    this.current_offhand_id = data.current_offhand.id
    this.current_right_ring_id = data.current_right_ring.id
  }
}
