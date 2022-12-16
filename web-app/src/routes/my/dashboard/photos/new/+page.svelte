<script>
  import { Input } from "$lib/components";
</script>

<div class="flex flex-col w-full h-full p-2">
  <div class="w-full">
    <form
      action="?/create"
      class="flex flex-col space-y-2 w-full items-center"
      enctype="multipart/form-data"
      method="POST"
    >
      <h3 class="text-3xl font-bold">Add a New Pet</h3>
      <p class="mt-2 text-lg">
        You can then assign this pet to feeders
      </p>
      <Input id="name" label="Pet Name" />
      <div class="form-control w-full max-w-lg">
        <label for="avatar" class="label font-medium pb-1">
            <span class="label-text">Avatar</span>
        </label>
        <input type="file" name="avatar" id="avatar" accept="image/*" class="file-input file-input-bordered file-input-secondary w-full max-w-lg" />
      </div>
      <div class="w-full max-w-lg pt-3">
        <button type="submit" class="btn btn-primary w-full max-w-lg">Add Pet</button>
      </div>
    </form>
  </div>
</div>
