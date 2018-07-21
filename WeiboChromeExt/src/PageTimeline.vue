<template lang="html">
  <div class="page-timeline svg-content" :style="trans">
      <div class="center-content">
        <nav-component></nav-component>
        <div class="main-content">
          <infomation-details :show-details="showDetails"
                              :show-data="showData"
                              :show-event="showEvent"
                              ></infomation-details>
          <div class="infomation-list">
             <transition-group name="list">
              <time-line-item
                v-for="(item,$index) in itemList"
                :class="item.klass"
                :dash-line-group="dashLineGroup"
                :item-data="item"
                :item-key="$index"
                :key="$index"
                :direction="direction"
              ></time-line-item>
            </transition-group>
          </div>
        </div>
      </div>
  </div>
</template>
<script>
import _ from 'lodash'
import * as d3 from 'd3'
import mapSVG from '../common/map'
import generatePolygon from '../common/generatePolygon'
import mapData from '../assets/data/map.json'
import {RANKOBJECT, RANKORDER, RANK} from '../common/variable'
import InfomationDetails from '../common/InfomationDetails'
import TimeLineItem from './TimeLineItem.vue'
import NavComponent from './NavComponent.vue'
import {showTimeInfomationDetails, hideTimeInfomationDetails} from './showDetails'
export default {
  name: 'PageMap',
  props: ['svgData'],
  data () {
    return {
      wheelInterval: 1300,
      wheelTimeStamp: +new Date(),
      statusIndex: 0,
      areaPos: [[250, 260], [450, 400], [120, 430], [250, 570], [630, 600], [400, 100], [440, 520], [550, 510]],
      showDetails: false,
      showData: {},
      dashLineGroup: {},
      showEvent: {},
      itemList: [],
      direction: 'down',
      hardReset: true,
      trans: '',
      init: {
        status0: false,
        status1: false,
        status2: false,
        status3: false,
        status4: false,
        status5: false,
        status6: false,
        status7: false,
        status8: false,
        status9: false,
        status10: false
      }
    }
  },
  activated () {
    this.wheelTimeStamp = +new Date()
    this.$emit('set:progress', '28.6%')
  },
  mounted () {
    let width = this.$el.clientWidth
    let height = width / 1.6
    let docWidth = window.document.body.clientWidth
    if (docWidth < 1300) {
      let scale = (width / 1280) > (height / 1000) ? (height / 1000) : (width / 1280)
      this.trans = `width:${width}px;height:${height}px;transform:scale(${scale}, ${scale})`
    }
    this.$nextTick(() => {
      this.render()
    })
  },
  methods: {
    processPreData () {
      let data = _.cloneDeep(this.svgData)
      let width = this.$el.querySelector('.main-content').clientWidth
      let r = 13
      let margin = {
        left: 80,
        right: 10,
        top: 100,
        bottom: 10
      }
      let colNum = 30
      let rowGap = 50
      let rowGapX = 1
      let rowGapY = 5
      this.prevMargin = margin
      this.prevR = r
      let groups = _.groupBy(data, 'rankCat')
      console.log(width)
      if (width === 1220) {
        r = 16
        rowGap = 60
        rowGapY = 5
        margin.top = 100
      }
      if (width === 1460) {
        r = 20
        rowGap = 100
        rowGapY = 8
        margin.top = 150
      }
      groups = _.omit(groups, '-')
      let arr = RANK.map((d, k) => {
        return {
          name: d[0],
          value: groups[d[0]],
          color: d[1]
        }
      })
      function getHeight (data) {
        let row = Math.ceil(data.length / colNum)
        return row * 2 * r + (row - 1) * rowGapY
      }
      function calculatePos (item, pos) {
        let t = arr.slice(0, pos)
        let preHeight = t.reduce((a, b) => {
          let h = a + getHeight(b.value, pos) + rowGap
          return h
        }, 0)
        item.value.forEach((d, i) => {
          let x = r + (i % 30) * 2 * (r + rowGapX)
          let y = preHeight + r + Math.floor(i / 30) * (2 * r + rowGapY) + margin.top
          d.pos = [x, y]
          d.color = item.color
        })
        item.topHeight = preHeight
      }
      arr.forEach((d, i) => {
        calculatePos(d, i)
      })
      let finalData = arr.reduce((a, b) => {
        return a.concat(b.value)
      }, [])
      return finalData
    },
    render () {
      let self = this
      let data = this.processPreData()
      let polygonData = _.cloneDeep(mapData)
      polygonData = polygonData.map(d => {
        let find = _.find(data, e => _.trim(e.name) === _.trim(d.name))
        return Object.assign(d, find)
      })
      let mapWidth = 680
      let mapHeight = 600
      let colNum = 30
      let rowGap = 10
      let rowGapX = 1
      let rowGapY = 5
      let width = this.$el.querySelector('.main-content').clientWidth
      let height = this.$el.querySelector('.main-content').clientHeight
      let r = 10
      let mapScale = 0.8
      let otherR = r * mapScale
      let otherTop = 560
      let mapPos = {
        left: 50,
        top: 50
      }
      let margin = {
        left: 0,
        right: 10,
        top: 0,
        bottom: 10
      }
      let areaGroup = _.groupBy(data, 'area')
      let otherData = []
      console.log(width)
      if (width === 1220) {
        r = 10
        mapWidth = 900
        mapHeight = 700
        mapScale = 1
        otherR = r * mapScale
        mapPos.top = 100
        otherTop = 630 + mapPos.top
      }
      if (width === 1460) {
        r = 10
        mapWidth = 1100
        mapHeight = 850
        mapScale = 1.4
        otherR = r * mapScale
        mapPos.top = 150
        otherTop = 880 + mapPos.top
      }
      otherData[0] = {
        name: '中央',
        value: _.reverse(_.sortBy(areaGroup['中央'], 'rankOrder'))
      }
      otherData[1] = {
        name: '企业',
        value: _.reverse(_.sortBy(areaGroup['企业'], 'rankOrder'))
      }
      otherData[2] = {
        name: '军队',
        value: areaGroup['军队']
      }
      otherData[3] = {
        name: '兵团',
        value: areaGroup['兵团']
      }
      function getHeight (data) {
        let row = Math.ceil(data.length / colNum)
        return row * 2 * otherR + (row - 1) * rowGapY
      }
      function calculatePos (item, pos) {
        let t = otherData.slice(0, pos)
        let preHeight = t.reduce((a, b) => {
          let h = a + getHeight(b.value, pos) + rowGap
          return h
        }, 0)
        item.value.forEach((d, i) => {
          let x = otherR + (i % 30) * 2 * (otherR + rowGapX) + margin.left + mapPos.left
          let y = preHeight + otherR + Math.floor(i / 30) * (2 * otherR + rowGapY) + margin.top + otherTop
          d.posNew = [x, y]
        })
        item.topHeight = preHeight
      }
      otherData.forEach((d, i) => {
        calculatePos(d, i)
      })
      let finalOtherData = otherData.reduce((a, b) => {
        return a.concat(b.value)
      }, [])
      let svg = d3.select(this.$el.querySelector('.main-content'))
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('baseProfile', 'tiny')
      .attr('version', '1.2')
      .attr('xmlns:ev', 'http://www.w3.org/2001/xml-events')
      .attr('xmlns:xlink', 'http://www.w3.org/1999/xlink')
      this.dashLineGroup = svg.append('g')
      let defs = svg.append('defs')
      defs.append('clipPath')
      .attr('id', 'clip')
      .append('rect')
      .attr('id', 'rect-clip')
      .attr('x', 0)
      .attr('y', 0)
      .attr('width', mapWidth)
      .attr('height', mapHeight)
      d3.select('body').on('click', (e) => {
        let klass = d3.select(d3.event.target).attr('class')
        console.log(klass)
        console.log(klass.indexOf('polygon-person'))
        if (!klass || (klass.indexOf('polygon-person') === -1 && klass.indexOf('avatar-person') === -1)) {
          this.showDetails = false
          d3.select('.rank-active-group').remove()
        }
      })
      let map
      function renderInitMaps () {
        let mapContainer = svg.append('g')
        .attr('class', 'map-container')
        mapContainer
        .attr('transform', `translate(0,${mapPos.top + margin.top})`)
        .attr('clip-path', 'url(#clip)')
        map = mapContainer.append('g')
        .attr('class', 'map')
        .attr('transform', `translate(0,0)`)
        map.html(mapSVG)
        .attr('font-size', 14)
        let chinaMap = map.select('.chinamap')
        chinaMap.style('opacity', 0)
        map
        .attr('transform', `translate(${mapPos.left}, 0)scale(${mapScale})`)
        chinaMap
        .style('opacity', 1)
        let persons = map.append('g')
        .attr('class', 'person-group')
        .selectAll('g')
        .data(polygonData)
        .enter()
        .append('g')
        .attr('class', 'person map-person polygon-person')
        .attr('transform', d => `translate(${d.grid[0]},${d.grid[1]})`)
        persons.append('polygon')
        .attr('points', d => {
          let p = generatePolygon([0, 0], r - 1, 6, Math.PI / 2)
          return p.map(d => d.join(',')).join(' ')
        })
        .attr('class', 'polygon-person')
        .attr('id', d => d.name)
        .attr('fill', d => d.color)
        .attr('stroke', d => {
          if (d.rankCat === '军队落马将领') {
            return '#000'
          } else {
            return '#fff'
          }
        })
        .attr('stroke-width', 1)
      }
      let otherPersons

      function renderOthers () {
        // render other polygon
        otherPersons = svg.append('g')
        .attr('class', 'other-person-group')
        .attr('transform', `translate(0, 0)`)
        // other legends
        otherPersons
        .append('g')
        .selectAll('text.legends')
        .data(otherData)
        .enter()
        .append('text')
        .attr('class', 'legends')
        .text(d => d.name + '：')
        .attr('x', margin.left)
        .attr('y', d => d.topHeight + margin.top + otherTop)
        .attr('dy', otherR + 4)
        .attr('fill', '#5A0F13')
        .attr('font-size', 14)
        let otherPolygons = otherPersons
        .append('g')
        .selectAll('g.other-person.person')
        .data(finalOtherData)
        .enter()
        .append('g')
        .attr('class', 'other-person person polygon-person')
        .attr('transform', d => `translate(${d.posNew[0]},${d.posNew[1]})`)
        otherPolygons.append('polygon')
        .attr('points', d => {
          let p = generatePolygon([0, 0], r - 1, 6, Math.PI / 2)
          return p.map(d => d.join(',')).join(' ')
        })
        .attr('id', d => d.name)
        .attr('fill', d => d.color)
        .attr('class', 'polygon-person')
        .attr('stroke', d => {
          if (d.rankCat === '军队落马将领') {
            return '#000'
          } else {
            return 'transparent'
          }
        })
        .attr('class', 'polygon-person')
        .attr('stroke-width', 1)
      }
      function renderInit () {
        renderInitMaps()
        renderOthers()
      }
      renderInit()
      svg.select('.chinamap')
      .transition(1000)
      .duration(1000)
      .style('opacity', 0)
      .on('end', () => {
        svg.select('.map-container').remove()
        svg.select('.other-person-group').remove()
        renderTimeLine.call(self)
      })

      polygonData.forEach(d => {
        let pos = d.grid
        pos = pos.map(d => d * mapScale)
        pos[0] = pos[0] + mapPos.left * mapScale
        pos[1] = pos[1] + mapPos.top
        d.mapPos = pos
      })
      finalOtherData.forEach(d => {
        d.mapPos = d.posNew
      })
      let all = polygonData.concat(finalOtherData)
      // ----------------------------------
      // timeline start
      function renderTimeLine () {
        let self = this
        let data = _.cloneDeep(this.svgData)
        let rankGap = 40
        let width = this.$el.querySelector('.main-content').clientWidth
        let timeLineHeight = 580
        let timeLineWidth = 600
        let margin = {
          left: 20,
          right: 10,
          top: 100,
          bottom: 10
        }
        let r = 8
        if (width === 1220) {
          r = 10
          timeLineWidth = 800
          margin.top = 100
        }
        if (width === 1460) {
          r = 12
          timeLineWidth = 1000
          timeLineHeight = 780
          margin.top = 150
        }
        let t = margin.top
        let dataGroupObj = _.groupBy(data, function (d) {
          var yearReg = /(\d{4})年/
          var matchs = d.falldownTime.match(yearReg)
          return matchs[1]
        })
        let dataGroup = _.toPairs(dataGroupObj)
        dataGroup.forEach(d => {
          let y = +new Date(d[0], 0, 1, 0, 0, 0)
          d[1].forEach(v => {
            v.year = y
          })
          let nums = d[1].filter(e => !_.isNaN(+e.rankOrder))
          nums = _.sortBy(nums, 'rankOrder')
          let strs = d[1].filter(e => _.isNaN(+e.rankOrder))
          strs = _.sortBy(strs, 'rankOrder')
          d[1] = nums.concat(strs)
          d[2] = y
        })
        let rankGroup = _.groupBy(data, 'rankCat')
        rankGroup = _.omit(rankGroup, '-')
        rankGroup = _.toPairs(rankGroup)
        let rankData = []
        function findOrder (name) {
          let find = _.find(rankGroup, function (d) {
            return d[0] === name
          })
          rankData.push(find)
        }
        _.each(RANKORDER, findOrder)
        _.each(rankData, function (d) {
          let n = _.groupBy(d[1], function (e) {
            let yearReg = /(\d{4})年/
            let matchs = e.falldownTime.match(yearReg)
            e.timeYear = +matchs[1]
            return matchs[1]
          })
          n = _.toPairs(n)
          let m = _.maxBy(n, function (e) {
            return e[1].length
          })
          let max = m[1].length
          let maxNumber = Math.ceil(max / 2)
          d[2] = maxNumber
        })
        rankData.reverse()
        let valueMax = d3.max(dataGroup.map(d => d[1].length))
        let valueExtent = [0, valueMax]
        let timeMin = d3.min(dataGroup.map(d => d[2]))
        let timeExtent = [timeMin, +new Date(2018, 0, 1, 0, 0)]
        let formatYear = d3.timeFormat('%Y')
        let y = d3.scaleLinear()
        .domain(valueExtent)
        .range([timeLineWidth, 0])
        let x = d3.scaleTime()
        .domain(timeExtent)
        .range([0, timeLineHeight])
        dataGroup.forEach(d => {
          let t = d[2]
          d[1].forEach((e, i) => {
            let py = y(i)
            let px = x(t)
            if (i % 2) {
              px = px + r
            }
            e.pos = [px, py]
            e.color = RANKOBJECT[e.rankCat]
          })
        })
        _.each(rankData, (d, i, all) => {
          let arr = all.slice(0, i)
          let sx = arr.reduce((a, b) => {
            return a + b[2] * 2 * r + rankGap
          }, 0)
          let dx = timeLineWidth - sx
          d[3] = dx
          // ----------------------------------
          let n = _.groupBy(d[1], function (e) {
            let yearReg = /(\d{4})年/
            let matchs = e.falldownTime.match(yearReg)
            e.timeYear = +matchs[1]
            return matchs[1]
          })
          n = _.toPairs(n)
          _.each(n, (e, i) => {
            let startY = x(new Date(+e[0], 0, 0, 0, 0, 0))
            let startX = dx
            _.each(e[1], (m, i) => {
              let dx = startX
              let dy = startY
              dx = dx - Math.floor((i / 2)) * 2 * r
              if (i % 4 === 0) {
                dy = dy + 0
              }
              if (i % 4 === 1) {
                dy = dy + 3 * r
              }
              if (i % 4 === 2) {
                dy = dy + r
              }
              if (i % 4 === 3) {
                dy = dy + 4 * r
              }
              m.rankPos = [dx, dy]
            })
          })
        })
        let finalData = dataGroup.reduce((a, b) => {
          return a.concat(b[1])
        }, [])

        finalData.forEach(d => {
          let o = _.find(all, e => e.name === d.name)
          let pos = o.mapPos
          pos[0] = pos[0] - margin.left + r
          pos[1] = pos[1] - margin.top
          d.mapPos = o.mapPos
        })
        console.log(finalData)
        let axisX = d3.axisRight(x)
            .tickPadding(5)
            .tickSizeOuter(3)
            .tickSizeInner(15)
            .tickFormat(d => {
              let year = +formatYear(d)
              if (year < 2017) {
                return year
              }
              if (year === 2017) {
                return year + '(年)'
              }
              return ''
            })
        let axisY = d3.axisTop(y)
          .tickPadding(10)
          .tickSizeInner(-timeLineHeight)
          .tickValues([0, 20, 40])
          .tickFormat(d => {
            if (d === 40) {
              return d + '(人)'
            }
            return d
          })
        d3.select('body').on('click', (e) => {
          let klass = d3.select(d3.event.target).attr('class')
          if (!klass || (klass.indexOf('polygon-person') === -1 && klass.indexOf('avatar-person') === -1)) {
            this.showDetails = false
            d3.select('.rank-active-group').remove()
          }
        })
        svg.append('text')
        .text('历年落马官员')
        .style('font-size', '18px')
        .style('font-weight', 'bold')
        .style('fill', 'rgb(91, 17, 17)')
        .attr('x', 0)
        .attr('y', 60)
        svg.append('g')
        .attr('class', 'axis axis-x')
        .attr('transform', `translate(${timeLineWidth + margin.left},${margin.top})`)
        .call(axisX)
        svg.append('g')
        .attr('class', 'axis axis-y')
        .attr('transform', `translate(${margin.left}, ${margin.top})`)
        .call(axisY)
        // content
        let rankLegends = svg.append('g')
        .attr('class', 'rank-legends')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        // content
        let personGroup = svg.append('g')
        .attr('class', 'person-group')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        let persons = personGroup
        .selectAll('g.person')
        .data(finalData)
        .enter()
        .append('g')
        .attr('class', 'person')
        .attr('transform', d => `translate(${d.mapPos[0] - r},${d.mapPos[1]})`)
        persons
        .transition()
        .duration(1000)
        .attr('transform', d => `translate(${d.pos[1] - r},${d.pos[0]})`)
        persons.append('polygon')
          .attr('points', d => {
            let p = generatePolygon([0, 0], r, 6, 0)
            return p.map(d => d.join(',')).join(' ')
          })
          .attr('id', d => d.name)
          .attr('fill', d => d.color)
          .attr('class', 'polygon-person')
          .attr('stroke', d => {
            if (d.rankCat === '军队落马将领') {
              return '#000'
            } else {
              return 'transparent'
            }
          })
          .attr('stroke-width', 1)
   // event bind ------------------------------------------
        svg.selectAll('.person')
        .on('click', function (d) {
          svg.selectAll('.rank-active-group').remove()
          hideTimeInfomationDetails()
          let dom = d3.select(this)
          let data = d3.range(6, r, r / 3)
          data = data.reverse()
          let activeGroup = dom
            .append('g')
            .attr('class', 'rank-active-group')
          activeGroup.selectAll('circle.rank-active')
            .data(data)
            .enter()
            .append('circle')
            .attr('class', 'rank-active')
            .attr('cx', 0)
            .attr('cy', 0)
            .attr('r', (d) => {
              return d
            })
            .attr('transform-origin', '0,0,')
            .attr('fill', '#5b1112')
            // show infomation
          self.showDetails = true
          self.showData = d
          self.showEvent = d3.event
        })
      // event bind  end------------------------------------------
        this.dashLineGroup = svg.append('g')
        .attr('class', 'dash-line-group')
        .attr('transform', `translate(${margin.left}, ${margin.top})`)
        let infomationList = [
          {
            time: +new Date(2012, 10, 0, 0, 0, 0),
            html: `2012年11月中共十八大召开。`,
            klass: 'em',
            top: t,
            left: 0
          },
          {
            time: +new Date(2012, 11, 4, 0, 0, 0),
            html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
            klass: 'em',
            top: t + 40,
            left: 0
          },
          {
            time: +new Date(2012, 11, 6, 0, 0, 0),
            html: `2012年12月6日中共中央纪委披露，四川省委副书记李春城涉嫌严重违纪接受组织调查，拉开中共十八大后“打老虎”的序幕。`,
            klass: 'em',
            top: t + 128,
            left: 0
          }
        ]
        function renderRecoverStatusOne () {
          svg.select('.axis.axis-y')
          .transition()
          .duration(1000)
          .attr('opacity', 1)
          persons
          .transition()
          .duration(1000)
          .delay((d, i) => i * 10)
          .attr('transform', d => `translate(${d.pos[1] - r},${d.pos[0]})`)
          showPopupPersonGroup
          .transition()
          .delay(1300)
          .duration(100)
          .attr('opacity', 1)
          rankLegends
          .transition()
          .duration(1000)
          .attr('opacity', 0)
        }
        function renderRank () {
          showPopupPersonGroup
          .transition()
          .duration(100)
          .attr('opacity', 0)
          svg.select('.axis.axis-y')
          .transition()
          .duration(1000)
          .attr('opacity', 0)
          rankLegends
          .transition()
          .duration(1000)
          .attr('opacity', 1)
          let rankLegendGroup = rankLegends.selectAll('g')
          .data(rankData)
          .enter()
          .append('g')
          .attr('transform', d => `translate(${d[3]}, 0)`)
          rankLegendGroup.append('text')
          .text(d => d[0])
          .attr('dx', '-0.5em')
          .attr('dy', '-0.5em')
          .style('text-anchor', 'end')
          rankLegendGroup.append('line')
          .attr('x1', 0)
          .attr('y1', 0)
          .attr('x2', 0)
          .attr('y2', d => timeLineHeight)
          .attr('class', 'split-line')
          persons
          .transition()
          .duration(1000)
          .delay((d, i) => i * 10)
          .attr('transform', d => `translate(${d.rankPos[0] - r},${d.rankPos[1]})`)
        }
        function getTargetPos (time) {
          let px = x(time)
          let py = timeLineWidth
          return [px, py]
        }
        infomationList.forEach(d => {
          d.pos = getTargetPos(d.time)
        })
        this.itemList = infomationList
        let showPopupPersonGroup = svg.append('g')
        .attr('class', 'showPopupPersonGroup')
        .attr('transform', `translate(${margin.left}, ${margin.top})`)
        function showDetailsPerson (name, pos) {
          let p = _.find(finalData, d => d.name === name)
          showTimeInfomationDetails(p, pos)
        }
        function showPopupPerson (name) {
          let person = _.find(finalData, d => d.name === name)
          let offset = 20
          let offsetY = 40
          let dx = 0
          let right = person.pos[1] + offset > timeLineWidth
          if (right) {
            offset = -60
            dx = 40
          }
          if (name === '徐才厚') {
            offset = -60
            dx = 40
          }
          if (name === '周永康') {
            offset = 0
          }
          if (name === '苏荣') {
            offset = 40
            dx = 0
          }
          if (name === '令计划') {
            offset = 60
            dx = 0
          }
          if (!showPopupPersonGroup.select(`#popup-${name}`).empty()) {
            return
          }
          showPopupPersonGroup.append('g')
          .attr('id', `popup-${name}`)
          showPopupPersonGroup.append('image')
          .attr('x', person.pos[1] + offset)
          .attr('y', person.pos[0] - 80)
          .attr('width', 40)
          .attr('height', 40)
          .attr('xlink:href', d => `static/avatar/${person.name}.png`)
          showPopupPersonGroup.append('path')
          .attr('stroke', '#000')
          .attr('stroke-width', 1)
          .attr('fill', 'none')
          .attr('d', d => {
            let p = person.pos
            if (right) {
              return `M${p[1] - r}, ${p[0]}Q${p[1]}  ${p[0] - offsetY}, ${p[1] + offset + dx}, ${p[0] - offsetY}`
            } else {
              return `M${p[1] - r}, ${p[0]}Q${p[1]}  ${p[0] - offsetY}, ${p[1] + offset + dx}, ${p[0] - offsetY}`
            }
          })
        }
        function renderSmallAvatar () {
          if (self.init.status1) {
            showPopupPerson('周永康')
          }
          if (self.init.status2) {
            showPopupPerson('徐才厚')
          }
          if (self.init.status3) {
            showPopupPerson('苏荣')
          }
          if (self.init.status4) {
            showPopupPerson('令计划')
          }
          if (self.init.status5) {
            showPopupPerson('郭伯雄')
          }
          if (self.init.status8) {
            showPopupPerson('孙政才')
          }
        }
        // ----------------------------------
        this.$el.addEventListener('mousewheel', (d) => {
          let now = +new Date()
          console.log(now - this.wheelTimeStamp)
          if (now - this.wheelTimeStamp < this.wheelInterval) {
            return
          } else {
            this.wheelTimeStamp = now
          }
          let index = this.statusIndex
          if (d.deltaY > 0) {
            this.direction = 'down'
            index++
            if (index > 10) {
              index = 10
              this.$router.push({
                name: 'PageCharges'
              })
            }
          } else {
            this.direction = 'up'
            index--
            if (index < 0) {
              index = 0
              this.$router.push({
                name: 'PageMap'
              })
            }
          }
          this.statusIndex = index
          this.showDetails = false
          renderSmallAvatar()
          hideTimeInfomationDetails()
          if (this.statusIndex === 0) {
            self.init.status0 = true
            this.hardReset = false
            this.itemList = infomationList
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 1) {
            renderRecoverStatusOne()
            self.init.status1 = true
            this.hardReset = false
            showDetailsPerson('周永康', {left: 20, top: -20})
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2012, 11, 6, 0, 0, 0),
                html: `2012年12月6日中共中央纪委披露，四川省委副书记李春城涉嫌严重违纪接受组织调查，拉开中共十八大后“打老虎”的序幕。`,
                klass: 'em',
                top: t + 128,
                left: 0
              },
              {
                time: +new Date(2014, 0, 0, 0, 0, 0),
                html: `2014年两会新闻发布会上，有记者向发言人吕新华询问前中央政治局常委周永康的消息，这位发言人回答称：<span class="quot">“我和你一样，在个别媒体上得到一些信息。无论什么人无论职位有多高，只要触犯党纪国法，就要严厉惩处。我只能回答成这样了，你懂的。”</span>一句“<span class="emp">你懂的</span>”引发舆论热议。`,
                klass: '',
                top: t + 230,
                left: 0
              },
              {
                time: +new Date(2014, 6, 29, 0, 0, 0),
                html: `2014年7月29日“你懂的”落地，中共中央决定对周永康严重违纪问题立案审查。`,
                klass: '',
                top: t + 380,
                left: 0
              },
              {
                time: +new Date(2014, 11, 5, 0, 0, 0),
                html: `2014年12月5日，中央政治局会议决定给予周永康开除党籍处分，对其涉嫌犯罪问题及线索移送司法机关依法处理。`,
                klass: '',
                top: t + 430,
                left: 0
              },
              {
                time: +new Date(2015, 5, 11, 0, 0, 0),
                html: `2015年6月11日，天津市第一中级人民法院依法对周永康受贿、滥用职权、故意泄露国家秘密案进行一审宣判，决定执行无期徒刑, 剥夺政治权利终身，并处没收个人财产。涉案金额1.3亿余元。财新曾发表周永康案<a href=" http://datanews.caixin.com/2014/zhoushicailu/" target="_blank" style="text-decoration:none;">长篇独家报道</a>。`,
                klass: '',
                top: t + 495,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
            // this.hardReset = true
          }
          if (this.statusIndex === 2) {
            renderRecoverStatusOne()
            self.init.status2 = true
            showDetailsPerson('徐才厚', {left: 0, top: 120})
            this.hardReset = false
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2014, 2, 15, 0, 0, 0),
                html: `2014年3月15日中共中央决定对<b>徐才厚</b>涉嫌违纪问题进行组织调查。`,
                klass: '',
                top: t + 215,
                left: 0
              },
              {
                time: +new Date(2015, 2, 15, 0, 0, 0),
                html: `2015年3月15日，由于徐才厚病亡，军事检察院对徐才厚作出不起诉决定，其涉嫌受贿犯罪所得依法处理。`,
                klass: '',
                top: t + 305,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 3) {
            renderRecoverStatusOne()
            showDetailsPerson('苏荣', {left: 0, top: 120})
            self.init.status3 = true
            this.hardReset = false
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2014, 5, 14, 0, 0, 0),
                html: `2014年6月14日经中共中央批准，中央纪委对<b>苏荣</b>进行立案审查。`,
                klass: '',
                top: t + 240,
                left: 0
              },
              {
                time: +new Date(2015, 1, 12, 0, 0, 0),
                html: `2015年2月12日，苏荣被双开。`,
                klass: '',
                top: t + 320,
                left: 0
              },
              {
                time: +new Date(2017, 0, 23, 0, 0, 0),
                html: `2017年1月23日，苏荣因受贿、滥用职权、巨额财产来源不明罪被判处无期徒刑，剥夺政治权利终身，并处没收个人全部财产。<b>涉案金额达1.9亿余元。</b>`,
                klass: '',
                top: t + 488,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 4) {
            renderRecoverStatusOne()
            this.hardReset = false
            self.init.status4 = true
            showDetailsPerson('令计划', {left: 0, top: 120})
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2014, 11, 22, 0, 0, 0),
                html: `2014年12月22日中共中央政治局决定对<b>令计划</b>立案审查。`,
                klass: '',
                top: t + 250,
                left: 0
              },
              {
                time: +new Date(2015, 6, 20, 0, 0, 0),
                html: `2015年7月20日，令计划被双开。`,
                klass: '',
                top: t + 320,
                left: 0
              },
              {
                time: +new Date(2016, 6, 4, 0, 0, 0),
                html: `2016年7月4日，天津市第一中级人民法院依法对令计划受贿、非法获取国家秘密、滥用职权案进行一审宣判，决定执行无期徒刑，剥夺政治权利终身，并处没收个人全部财产。<b>涉案金额达7700万余元</b>。`,
                klass: '',
                top: t + 370,
                left: 0
              },
              {
                time: +new Date(2016, 6, 25, 0, 0, 0),
                html: `令计划之兄<b>令政策</b>已在2014年山西腐败案中落马，其弟令完成借助兄长们的权势攫财，在令政策案发后藏身美国。如今处于舆论中央的乐视，数年来关于其如何能成功上市的质疑一直没断过，而这起著名的IPO当年亦有令完成的身影出没其间。`,
                klass: '',
                top: t + 480,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 5) {
            renderRecoverStatusOne()
            this.hardReset = false
            showDetailsPerson('郭伯雄', {left: 0, top: 120})
            self.init.status5 = true
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2015, 3, 12, 0, 0, 0),
                html: `2015年4月9日中共中央决定对<b>郭伯雄</b>进行组织调查。`,
                klass: '',
                top: t + 270,
                left: 0
              },
              {
                time: +new Date(2015, 6, 30, 0, 0, 0),
                html: `7月30日，中央政治局会议决定给予郭伯雄开除党籍处分，对其涉嫌严重受贿犯罪问题及线索移送最高人民检察院授权军事检察机关依法处理。`,
                klass: '',
                top: t + 340,
                left: 0
              },
              {
                time: +new Date(2016, 6, 25, 0, 0, 0),
                html: `2016年7月25日，军事法院依法对郭伯雄受贿案进行一审宣判，判处无期徒刑，剥夺政治权利终身，并处没收个人全部财产，剥夺上将军衔。`,
                klass: '',
                top: t + 440,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 6) {
            renderRecoverStatusOne()
            this.hardReset = false
            this.showDetails = false
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2015, 2, 0, 0, 0, 0),
                html: `3月，时任中共中央政治局常委、中央纪委书记王岐山在当年两会上强调，管党治党靠党内规则、严明纪律。依规治党首先要把党规党纪的篱笆扎紧，<b>把领导干部的权力关进制度的笼子</b>。要抓早抓小，触犯了纪律就要及时处理，决不能放任自流，造成干部要么是“<span class="emp">好同志</span>”、要么是“<span class="emp">阶下囚</span>”。`,
                klass: '',
                top: t + 265,
                left: 0
              },
              {
                time: +new Date(2015, 8, 0, 0, 0, 0),
                html: `9月，王岐山提出纪委监督执纪“<span class="emp">四种形态”</span>，即党内关系要正常化，批评和自我批评要经常开展，让咬耳扯袖、红脸出汗成为常态；党纪轻处分和组织处理要成为大多数；对严重违纪的重处分、作出重大职务调整应当是少数；严重违纪涉嫌违法立案审查的只能是极少数。`,
                klass: '',
                top: t + 440,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 7) {
            renderRecoverStatusOne()
            this.hardReset = false
            this.showDetails = false
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2016, 0, 0, 0, 0, 0),
                html: `2016年落马高官宣判迎来高潮，总数逼近前两年总和的两倍：重庆人大常委会原副主任谭栖伟开启2016高官宣判季；涉周永康案“大老虎”李东生、冀文林年初结案；令计划、郭伯雄年中落槌；山西窝案下半年悉数宣判，地方“<span class="emp">首虎</span>”密集领刑。`,
                klass: '',
                top: t + 270,
                left: 0
              },
              {
                time: +new Date(2016, 1, 0, 0, 0, 0),
                html: `2016年1月，十八届中央纪委六次全会召开。习近平强调，<b>反腐败斗争压倒性态势正在形成</b>。要“<span class="quot">强化党内监督，着力解决群众身边的不正之风和腐败问题，坚决遏制腐败蔓延势头。</span>”`,
                klass: '',
                top: t + 420,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 8) {
            renderRecoverStatusOne()
            showDetailsPerson('孙政才', {left: 0, top: 0})
            self.init.status8 = true
            this.hardReset = false
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2017, 0, 0, 0, 0, 0),
                html: `2017年1月，十八届中央纪委七次全会召开。习近平强调，腐败蔓延势头得到有效遏制，<b>反腐败斗争压倒性态势已经形成</b>。“<span class="quot">不敢腐的目标初步实现，要继续在常和长、严和实、深和细上下功夫，不断增强全面从严治党的系统性、创造性、实效性。</span>”`,
                klass: '',
                top: t + 135,
                left: 0
              },
              {
                time: +new Date(2017, 6, 24, 0, 0, 0),
                html: `2017年7月24日中共中央决定对十八届中央政治局委员<b>孙政才</b>涉嫌严重违纪问题立案审查。9月29日，中央政治局会议决定给予孙政才开除党籍、开除公职处分，将其涉嫌犯罪问题及线索移送司法机关依法处理。`,
                klass: '',
                top: t + 285,
                left: 0
              },
              {
                time: +new Date(2017, 7, 0, 0, 0, 0),
                html: `中共十九大召开前夕，反腐 “<span class="emp">去库存</span>”加速，中央陆续宣布对重庆原副市长、公安局原局长<b>何挺</b>，重庆原副市长<b>沐华平</b>，公安部原政治部主任<b>夏崇源</b>，司法部原部长<b>吴爱英</b>四人的党纪处分。此外，中央军委后勤保障部原副部长<b>刘生杰</b>中将被撤中央纪委委员，成为十八届中央纪委产生后第七名被处分的中央纪委委员。`,
                klass: '',
                top: t + 435,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 9) {
            renderRecoverStatusOne()
            this.hardReset = false
            this.showDetails = false
            let list = [
              {
                time: +new Date(2012, 10, 0, 0, 0, 0),
                html: `2012年11月中共十八大召开。`,
                klass: 'em',
                top: t,
                left: 0
              },
              {
                time: +new Date(2012, 11, 4, 0, 0, 0),
                html: `2012年12月4日中共中央政治局会议审议通过《十八届中央政治局关于改进工作作风、密切联系群众的八项规定》。`,
                klass: 'em',
                top: t + 40,
                left: 0
              },
              {
                time: +new Date(2017, 0, 0, 0, 0, 0),
                html: `2017年1月，十八届中央纪委七次全会召开。习近平强调，腐败蔓延势头得到有效遏制，<b>反腐败斗争压倒性态势已经形成</b>。“<span class="quot">不敢腐的目标初步实现，要继续在常和长、严和实、深和细上下功夫,不断增强全面从严治党的系统性、创造性、实效性。</span>”`,
                klass: 'em',
                top: t + 227,
                left: 0
              },
              {
                time: +new Date(2017, 0, 0, 0, 0, 0),
                html: `至此，从李春城到孙政才，五年187名副省级以上高官落马。`,
                klass: 'em',
                top: t + 364,
                left: 0
              },
              {
                time: +new Date(2017, 9, 18, 0, 0, 0),
                html: `2017年10月18日，中共十九大召开。`,
                klass: 'em',
                top: t + 420,
                left: 0
              },
              {
                time: +new Date(2018, 0, 0, 0, 0, 0),
                html: `习近平在十九大报告《决胜全面建成小康社会 夺取新时代中国特色社会主义伟大胜利》中提到：“<span class="quot">坚持反腐败无禁区、全覆盖、零容忍，坚定不移‘打虎’、‘拍蝇’、‘猎狐’，不敢腐的目标初步实现，不能腐的笼子越扎越牢，不想腐的堤坝正在构筑，<b>反腐败斗争压倒性态势已经形成并巩固发展</b>。</span>”`,
                klass: 'em',
                top: t + 460,
                left: 0
              }
            ]
            list.forEach(d => {
              d.pos = getTargetPos(d.time)
            })
            this.itemList = list
            this.$nextTick(() => {
              this.hardReset = true
            })
          }
          if (this.statusIndex === 10) {
            this.itemList = []
            renderRank()
          }
          console.log(this.statusIndex)
        })
      }
      // ------------------------------------
    }
  },
  components: {
    InfomationDetails,
    NavComponent,
    TimeLineItem
  }
}
</script>
<style lang="scss">
  .page-map{
    width: 100%;
    height: 100%;
    position: relative;
      .infomation-list{
        position: absolute;
        right: 0;
        top: 0;
        bottom:0;
        width: 300px;
      }
      .cannotclickable:hover{
        cursor: default !important;
      }
  }

  .title{
    top: 15px;
  }
  .person polygon:hover{
    cursor: pointer;
  }

  .other-label{
    fill: #5b1112;
  }
  .item{
    position: absolute;
    left:0;
    top:0;
    right:0;
    width: 100%;
    padding: 3px 5px 3px 15px;
    border-left:3px solid  #5b1112;
    color: #5b1112;
    background: #F7F3F3;
    line-height: 2;
    font-size: 12px;
    margin-bottom:5px;
    b{
      color: #000;
    }
  }
  .item.em{
    background: #DECFD0;
  }
  .quote{
    position: absolute;
    left:0;
    top:0;
    right:0;
    width: 100%;
    padding: 10px 5px 10px 15px;
    display: flex;
    flex-flow: row nowrap;
    align-items: center;
    color: #5b1112;
    background: url('../assets/img/quote-left.png') left top no-repeat, url('../assets/img/quote-right.png') right bottom no-repeat;
    background-color: #F7F3F3;
    margin-bottom:5px;
    font-size: 12px;
    overflow: hidden;
    p {
      width: 170px;
    }
    img {
      width: 100px;
      margin-left: 10px;
    }
  }

    // map setting
    .china-map .map-chart {
      flex: 1;
      width: 100%;
      background-size: 100%;
    }

    .china-map .map-area {
      height: 0.5rem;
      line-height: 0.5rem;
      width: 100%;
      padding: 0 0.25rem;
      font-size: 10px;
      color: #5B1112;

    }
    .person polygon,
    .province {
      transition: all 1s;
    }
    .province:hover,
    .data-polygon:hover {
      cursor: pointer;
    }
    .indicate-line.st11{
      stroke:#000000;
    }
    .province.lighter{
      opacity: 0.2;
    }
  	.st0{fill:#5B1111;stroke:#FFFFFF;stroke-width:0.5;stroke-miterlimit:10;}
  	.st1{fill-rule:evenodd;clip-rule:evenodd;fill:#5B1111;stroke:#FFFFFF;stroke-width:0.5;stroke-miterlimit:10;}
  	.st2{fill:#5B1111;}
  	.st3{fill:none;stroke:#FFFFFF;stroke-width:0.5;stroke-miterlimit:10;}
  	.st4{display:none;}
  	.st5{display:inline;fill:#EBEBEB;}
  	.st6{display:inline;fill:#FFFFFF;}
  	.st7{display:inline;fill:#B0B0B0;}
  	.st8{display:inline;fill:#757575;}
  	.st9{display:inline;fill:#666666;stroke:#FFFFFF;stroke-miterlimit:10;}
  	.st10{display:inline;fill:#4D4D4D;}
  	.st11{display:inline;fill:#999999;stroke:#FFFFFF;stroke-miterlimit:10;}
  	.st12{display:inline;fill:none;stroke:#000000;stroke-miterlimit:10;}
    </style>

<style lang="scss">
    .extra-information {
      position: absolute;
      width: 250px;
      padding: 15px;
      color: #5B1111;
      background: #DECFD0;
    }
    .popup-person {
      position: absolute;
      top: 0;
      left: 0;
      width: 330px;
      .avatar-img {
        float: left;
        width: 100px;
        img{
          width: 100%;
          max-width: 100%;
        }
      }
      .popup-info{
        float: left;
        width: 220px;
        min-height: 100px;
        padding: 5px;
        color :#5b1111;
        line-height: 1.5;
        border:1px solid #5B1111;
        margin-left: 10px;
        box-shadow: 0 0 3px 3px rgba(90,15,19, 0.3);
        background-color: #fff;
        .person-name{
          margin-bottom: 5px;
          padding-bottom: 5px;
          border-bottom: 1px solid #5b1111;
        }
        b{
          color: #000;
        }
      }
    }

    .popup-person.hide {
        width: 100px;
        .popup-info {
          display: none;
        }
        .avatar-img img {
          transition: 0.5s all linear;
          transform-origin: left bottom;
          transform: scale(0.5);
        }
    }
    .page-timeline {
      width: 100%;
      height: 100%;
      position: relative;
      background: #fff;
      .time-dash-line{
        stroke:#5B1111;
        stroke-dasharray: 3px;
        stroke-width: 1px;
      }
      .infomation-list{
        position: absolute;
        right:0;
        top: 0;
        bottom:0;
        width: 300px;
        font-size: 12px;
      }
      .item{
        position: absolute;
        width: 100%;
        padding: 3px 5px 3px 15px;
        border-left:3px solid  #5b1112;
        color: #5b1112;
        background: #F7F3F3;
        line-height: 1.5;
        margin-bottom:5px;
        b{
          color: #000;
        }
      }
      .item.em{
        background: #DECFD0;
        font-weight: 400;
      }
      .quote{
        width: 100%;
        padding: 10px 5px 10px 15px;
        background: url('../assets/img/quote-left.png') left top no-repeat, url('../assets/img/quote-right.png') right bottom no-repeat;
        background-color: #F7F3F3;
        margin-bottom:5px;
        overflow: hidden;
        color: #5b1112;
        p {
          width: 170px;
          float: left;
        }
        img {
          width: 100px;
          float: left;
          margin-left: 10px;
        }
      }

      .person polygon:hover{
        cursor: pointer;
      }
      .axis-x .tick line{
        stroke-width: 1px;
        stroke: #5B1111;
      }
      .axis.axis-x path {
        stroke-width: 5px;
        stroke: #5B1111;
      }
      .axis text{
        font-size: 14px;
        fill: #5B1111;
      }
      .axis.axis-y path {
        display: none;
      }
      .split-line{
        stroke-width: 1px;
        stroke: #5B1111;
      }
    }

    .infomation-wrapper {
      position: absolute;
      left:22px;
      top:25px;
      padding: 5px;
      z-index:1000;
      width: 310px;
      max-width: 310px;
      font-size: 12px;
      background: #fff;
      color: #5B1111;
      border: 1px solid #5B1111;
      box-shadow: 3px 3px 3px rgba(0,0,0,0.5),  0 0 2px 2px rgba(144,50,50,0.8);
      transition: all 0.3s linear;
      .information-name {
        padding-bottom: 5px;
        margin-bottom: 5px;
        border-bottom:1px solid #5B1112;
      }
      .information-name b{
        margin-right: 0.5em;
        font-size: 14px;
        color: #000;
      }
      .avatar{
        width: 80px;
        float: left;
        overflow: hidden;
        margin-right: 10px;
        img{
          max-width: 100%;
        }
      }
      .text {
        width: 200px;
        float: left;
        overflow: hidden;
      }
      .information-details   p {
        line-height: 1.5;
      }
    }
    .page-timeline {
      // map setting
      .china-map .map-chart {
        flex: 1;
        width: 100%;
        background-size: 100%;
      }

      .china-map .map-area {
        height: 0.5rem;
        line-height: 0.5rem;
        width: 100%;
        padding: 0 0.25rem;
        font-size: 10px;
        color: #5B1112;

      }
      .person polygon,
      .province {
        transition: all 3s;
      }
      .province:hover,
      .data-polygon:hover {
        cursor: pointer;
      }
      .indicate-line.st11{
        stroke:#000000;
      }
      .province.lighter{
        opacity: 0.2;
      }
      .st0{fill:#5B1111;stroke:#FFFFFF;stroke-width:0.5;stroke-miterlimit:10;}
      .st1{fill-rule:evenodd;clip-rule:evenodd;fill:#5B1111;stroke:#FFFFFF;stroke-width:0.5;stroke-miterlimit:10;}
      .st2{fill:#5B1111;}
      .st3{fill:none;stroke:#FFFFFF;stroke-width:0.5;stroke-miterlimit:10;}
      .st4{display:none;}
      .st5{display:inline;fill:#EBEBEB;}
      .st6{display:inline;fill:#FFFFFF;}
      .st7{display:inline;fill:#B0B0B0;}
      .st8{display:inline;fill:#757575;}
      .st9{display:inline;fill:#666666;stroke:#FFFFFF;stroke-miterlimit:10;}
      .st10{display:inline;fill:#4D4D4D;}
      .st11{display:inline;fill:#999999;stroke:#FFFFFF;stroke-miterlimit:10;}
      .st12{display:inline;fill:none;stroke:#000000;stroke-miterlimit:10;}
    }
    .quot{
      font-family: 'STKaiti';
    }
    .emp{
      font-weight: 400;
    }
    </style>
