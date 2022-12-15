const { randomBytes } = await import('node:crypto')

export const serialiseNonPojos = (obj) => {
    return structuredClone(obj)
}

export const generateUsername = (name) => {
    const id = randomBytes(2).toString('hex')
    return `${name.slice(0, 5)}${id}`
}

export const getImageUrl = (collectionId, recordId, filename, size = '0x0') => {
    return `https://clever-cat-pb.eoinfennessy.com/api/files/${collectionId}/${recordId}/${filename}?thumb=${size}`;
}