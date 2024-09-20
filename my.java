public class UploadImageAdapter extends RecyclerView.Adapter<UploadImageAdapter.UploadImageViewHolder> {
    // ...
    @NonNull
    @Override
    public UploadImageViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(mContext).inflate(R.layout.upload_image_block, parent, false);
        return new UploadImageViewHolder(v);
    }

    @SuppressLint("SetTextI18n")
    public void onBindViewHolder(@NonNull UploadImageAdapter.UploadImageViewHolder holder, int position) {
        Upload uploadCurrent = mUploads.get(position);
        holder.textViewName.setText("Изображение " + (mUploads.size()-position));
        
        // Загрузка изображения с помощью Glide
        Glide.with(mContext.getApplicationContext())
            .load(uploadCurrent.getImageUrl())
            .centerCrop()
            .into(holder.imageView);

        // Обработчики кликов
        holder.textViewName.setOnClickListener(v -> {
            try {
                onStateClickListenerUpload.onClickAdd(uploadCurrent);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
        holder.imageView.setOnClickListener(v -> {
            try {
                onStateClickListenerUpload.onClickAdd(uploadCurrent);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });

        holder.deleteButton.setOnClickListener(v -> {
            try {
                onStateClickListenerDelete.onClickAdd(uploadCurrent, position);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
    }
}
