<template>
  <div class="timeline-loader-view">
    <div class="timeline-loader--time-slot"></div>
    <div class="timeline-loader--newsletter-heading"></div>
    <div class="timeline-loader--newsletter-info">
      <div class="timeline-loader--newsletter-info--img"></div>
    </div>

    <div class="timeline-loader--post" v-for="x in 2" :key="x">
      <div class="timeline-loader--post--header">
        <div class="timeline-loader--post--header--img"></div>
      </div>
      <div class="timeline-loader--post--heading"></div>
      <div class="timeline-loader--post--content">
        <div class="text-lines" v-for="y in 26" :key="y"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TimelineLoader'
}
</script>

<style lang="sass">
.timeline-loader--time-slot
  display: flex
  align-items: center
  justify-content: center
  height: $baseline * 1.5

  &::before
    height: $baseline * 1.25 
    width: 200px

    animation: pulse-darker 1s infinite ease-in-out
    background: #ddd

    content: ''

.timeline-loader--newsletter-heading
  display: flex
  align-items: center
  justify-content: center
  height: $baseline * 1.25
  margin: $baseline 0 $baseline/4
  
  &::before
    height: $baseline * 1 
    width: 300px

    animation: pulse-darker 1s infinite ease-in-out
    background: #ddd

    content: ''

    @media (max-width: $mobile)
      width: 250px

.timeline-loader--newsletter-info
  display: flex
  align-items: center
  justify-content: center
  height: $baseline
  margin-bottom: $baseline
  
  &::after
    height: $baseline * 0.6
    width: 400px

    animation: pulse-darker 1s infinite ease-in-out
    background: #ddd

    content: ''

    @media (max-width: $mobile)
      width: 300px

.timeline-loader--newsletter-info--img
  border-radius: 100%
  height: $baseline
  margin-right: $baseline / 8
  width: $baseline

  animation: pulse-darker 1s infinite ease-in-out
  background: #ddd

  

.timeline-loader--post
  margin-bottom: $baseline / 2
  padding: $baseline / 2

  background: #fff

  @media (max-width: $mobile)
    padding: $baseline / 4

.timeline-loader--post--header
  display: flex
  align-items: center
  height: $baseline
  margin-bottom: $baseline / 4

  &::after
    height: $baseline * 0.5
    width: 200px

    animation: pulse 1s infinite ease-in-out
    background: #eee

    content: ''

.timeline-loader--post--header--img
  border-radius: 100%
  height: $baseline
  margin-right: $baseline / 8
  width: $baseline

  animation: pulse 1s infinite ease-in-out
  background: #eee

.timeline-loader--post--heading
  display: flex
  align-items: center
  height: $fs-1 * 1.58
  margin-bottom: $baseline / 8

  &::after
    height: $baseline
    width: 90%

    animation: pulse 1s infinite ease-in-out
    background: #eee

    content: ''

.timeline-loader--post--content
  display: grid
  grid-template-columns: 1fr 1fr 1fr

  @media (max-width: $mobile)
    grid-template-columns: 1fr 1fr

  .text-lines
    display: flex
    align-items: center
    height: 15px * 1.6

    &::after
      height: $baseline * 0.5

      animation: pulse 1s infinite ease-in-out
      background: #eee

      content: ''

    &:nth-of-type(odd)::after
      width: 70%

    &:nth-of-type(even)::after
      width: 80%

    &:nth-of-type(4n + 1)::after,
    &:nth-of-type(4n + 2)::after
      @media (max-width: $mobile)
        width: 70%

    &:nth-of-type(4n + 3)::after,
    &:nth-of-type(4n + 4)::after
      @media (max-width: $mobile)
        width: 80%

  @keyframes pulse
    0%
      background-color: #eee
    50% 
      background-color: #e5e5e5
    100%
      background-color: #eee

  @keyframes pulse-darker
    0%
      background-color: #ddd
    50% 
      background-color: #d5d5d5
    100%
      background-color: #ddd
</style>