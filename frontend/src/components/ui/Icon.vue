<script setup lang="ts">

withDefaults(
    defineProps<{
      icon?: string,
      size?: number
    }>(),
    {
      size: 19
    }
)

</script>

<template>
  <svg xmlns="http://www.w3.org/2000/svg" :width="size" :height="size" :viewBox="'0 0 ' + size + ' ' + size" fill="none">
    <g v-if="icon === 'Brand'">
      <path d="M1.75 7.875L10.5 3.5L19.25 7.875L10.5 12.25L1.75 7.875Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M5.25 9.625V14C7.875 16.625 13.125 16.625 15.75 14V9.625M19.25 7.875V13.125" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-if="icon === 'House'">
      <path d="M2.38086 7.92155L9.50586 2.37988L16.6309 7.92155" stroke="#C6D4CF" stroke-width="1.425" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M3.96094 7.12988V15.8382H15.0443V7.12988M7.1276 15.8382V10.2965H11.8776V15.8382" stroke="#C6D4CF" stroke-width="1.425" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-else-if="icon === 'Book'">
      <path d="M3.16602 15.4374C3.16602 14.9125 3.37453 14.4091 3.7457 14.0379C4.11687 13.6668 4.62027 13.4583 5.14518 13.4583H15.8327" stroke="#C6D4CF" stroke-width="1.425" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M5.14518 1.58325H15.8327V17.4166H5.14518C4.62027 17.4166 4.11687 17.2081 3.7457 16.8369C3.37453 16.4657 3.16602 15.9623 3.16602 15.4374V3.56242C3.16602 3.03751 3.37453 2.5341 3.7457 2.16294C4.11687 1.79177 4.62027 1.58325 5.14518 1.58325Z" stroke="#C6D4CF" stroke-width="1.425" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-else-if="icon === 'Upload'">
      <path d="M9.49935 12.6667V3.16675M13.4577 7.12508L9.49935 3.16675L5.54102 7.12508" stroke="#C6D4CF" stroke-width="1.425" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M15.8327 11.875V15.8333H3.16602V11.875" stroke="#C6D4CF" stroke-width="1.425" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-else-if="icon === 'Download'">
      <path d="M8.49992 2.125V11.3333M12.0416 7.79167L8.49992 11.3333L4.95825 7.79167" stroke="#173F35" stroke-width="1.275" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M3.54175 14.875H13.4584" stroke="#173F35" stroke-width="1.275" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-else-if="icon === 'Arrow'">
      <path d="M3.45911 8.99984H14.5424M10.5841 12.9582L14.5424 8.99984L10.5841 5.0415" stroke="#C6D4CF" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-else-if="icon === 'Door'">
      <path d="M7.0835 2.83331H2.8335V14.1666H7.0835M9.91683 11.3333L12.7502 8.49998L9.91683 5.66665M12.7502 8.49998H5.66683" stroke="#9DB4AB" stroke-width="1.275" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-else-if="icon === 'Eye'">
      <path d="M1.41675 8.5C1.41675 8.5 3.89591 4.25 8.50008 4.25C13.1042 4.25 15.5834 8.5 15.5834 8.5C15.5834 8.5 13.1042 12.75 8.50008 12.75C3.89591 12.75 1.41675 8.5 1.41675 8.5Z" stroke="#173F35" stroke-width="1.275" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M8.50008 10.2708C9.47809 10.2708 10.2709 9.47796 10.2709 8.49996C10.2709 7.52196 9.47809 6.72913 8.50008 6.72913C7.52208 6.72913 6.72925 7.52196 6.72925 8.49996C6.72925 9.47796 7.52208 10.2708 8.50008 10.2708Z" stroke="#173F35" stroke-width="1.275" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-else-if="icon === 'Report'">
      <path d="M3.33325 14V2.66663" stroke="#173F35" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M3.33325 3.33337H10.6666L9.99992 6.00004L11.9999 8.00004H3.33325" stroke="#173F35" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

    <g v-else-if="icon === 'Search'">
      <path d="M9.625 15.75C13.0077 15.75 15.75 13.0077 15.75 9.625C15.75 6.24226 13.0077 3.5 9.625 3.5C6.24226 3.5 3.5 6.24226 3.5 9.625C3.5 13.0077 6.24226 15.75 9.625 15.75Z" stroke="#17211B" stroke-width="1.575" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M17.5 17.5L14 14" stroke="#17211B" stroke-width="1.575" stroke-linecap="round" stroke-linejoin="round"/>
    </g>

  </svg>

</template>