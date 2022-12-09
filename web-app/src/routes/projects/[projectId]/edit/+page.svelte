<script>
    export let data;
</script>

<div class="flex flex-col w-full p-2">
    <div class="w-full">
        <form method="POST" action="?/updateProject" class="flex flex-col space-y-2 w-full items-center" enctype="multipart/form-data">
            <h3 class="text-3xl font-bold">
                Edit {data.project.name}
            </h3>
        </form>
    </div>
</div>