<template>
  <read-later-widget>
    <div>
      Article is saved in your Reading List. Do you want to remind it?

      <read-later-widget--buttons>
        <button v-on:click="closeReadLaterMessage()">In 1 hour</button>
        <button v-on:click="closeReadLaterMessage()">Tomorrow</button>
        <button v-on:click="closeReadLaterMessage()">Next week</button>
      </read-later-widget--buttons>

      <read-later-widget--close-button
        v-on:click="closeReadLaterMessage()"
        aria-label="Close Dialog">
      </read-later-widget--close-button>
    </div>
  </read-later-widget>
</template>

<script>

export default {
  name: 'ReadLaterWidget',
  methods: {
    closeReadLaterMessage: function () {
      this.$emit('readlaterwidgetclose');
    }
  }
}
</script>