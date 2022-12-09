<script>
  import { Icon, Pencil } from "svelte-hero-icons";
  import { Input } from "$lib/components";
  import { getImageUrl } from '$lib/utils';
  import { invalidateAll } from "$app/navigation";
  import { applyAction, enhance } from "$app/forms";

  export let data;
  let loading;
  $: loading = false;

  let avatarSrc;
  if (data.user?.avatar) {
    avatarSrc = getImageUrl(data.user.collectionId, data.user.id, data.user.avatar, '300x300')
  } else {
    avatarSrc = `https://ui-avatars.com/api/?name=${data.user?.name}`;
  }

  const previewAvatar = (event) => {
    const files = event.target.files;
    if (files) {
      avatarSrc = URL.createObjectURL(files[0]);
    }
  };

  const submitUpdateProfile = () => {
    loading = true;
    return async ({ result }) => {
      switch (result.type) {
        case 'success':
          await invalidateAll();
          break;
        case 'error':
          break;
        default:
          await applyAction(result);
      }
      loading = false;
    }
  }
</script>

<div class="flex flex-col w-full h-full">
  <form
    action="?/updateProfile"
    method="POST"
    class="flex flex-col space-y-2 w-full"
    enctype="multipart/form-data"
    use:enhance={submitUpdateProfile}
  >
    <h3 class="text-2xl font-medium">Update Profile</h3>
    <div class="form-control w-full max-w-lg">
      <label for="avatar" class="label font-medium pb-1">
        <span class="label-text">Profile Picture</span>
      </label>
      <label for="avatar" class="avatar w-32 rounded-full hover:cursor-pointer">
        <label
          for="avatar"
          class="absolute -bottom-0.5 -right-0.5 hover:cursor-pointer"
        >
          <span class="btn btn-circle btn-sm btn-secondary">
            <Icon src={Pencil} class="w-4 h-4" />
          </span>
        </label>
        <div class="w-32 rounded-full">
          <img src={avatarSrc} alt="user avatar" />
        </div>
      </label>
      <input
        type="file"
        name="avatar"
        id="avatar"
        value=""
        accept="image/*"
        on:change={previewAvatar}
        hidden
        disabled={loading}
      />
    </div>
    <Input id="name" label="Name" value={data?.user?.name} disabled={loading} />
    <div class="w-full max-w-lg pt-3">
      <button class="btn btn-primary w-full max-w-lg" type="submit" disabled={loading}>
        Update Profile
      </button>
    </div>
  </form>
</div>
