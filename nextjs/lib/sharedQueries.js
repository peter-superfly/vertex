import { gql } from "@apollo/client";

export const SubscribeToAccount = gql`
    subscription SubscribeToAccount($username: String!) {
        accounts_by_pk(username: $username) {
            uid
            bio
            username
            title
            email
            fullname
            bg_color
            banner_url
            avatar_url
            created_at
            last_seen
            updated_at
            last_login
            phone
            theme
            blocks(order_by: {page_row_idx: asc}) {
              text
              uid
              type
              image_url
              owner_uid
               page_row_idx
            }
            block_types{
              type
              id
            }
            bg_colors{
              hex
              name
              id
            }
            social_accounts_types{
              id
              url
              name
            }
            themes {
              id
              name
              key
            }
          }
    } 
`

export const SubscribeToBlocks = gql`
    subscription SubscribeToAccountBlocks($owner_uid: uuid!) {
        blocks(where: {owner_uid: {_eq: $owner_uid}}, order_by: {page_row_idx: asc}) {
          text
          uid
          type
          owner_uid
          page_row_idx
          image_url
        }
    }
`

export const GetAccount = gql`
    query GetAccount($username: String!) {
      accounts(where: {username: {_eq: $username}}) {
        uid
        bio
        username
        title
        email
        fullname
        bg_color
        avatar_url
        banner_url
        created_at
        last_seen
        updated_at
        last_login
        phone
        theme
        blocks(order_by: {page_row_idx: asc}) {
          text
          uid
          type
          owner_uid
          page_row_idx
          image_url
        }
      }
      block_types {
        type
        id
      }
      bg_colors {
        hex
        name
        id
      }
      social_accounts_types {
        id
        url
        name
      }
      themes {
        id
        name
        key
      }
    }
`;

export const UpdateAccount = gql`
    mutation UpdateAccount(
        $uid: uuid!,
        $fullname: String!,
        $bio: String!,
        $title: String!,
        $email: String!
      ) {
      update_accounts(
        where: { uid: { _eq: $uid } }
        _set: {
            email: $email,
            fullname: $fullname,
            title: $title,
            bio: $bio
        }
      ) {
        affected_rows
        returning {
          uid
          fullname
          email
          title
          bio
        }
      }
    }
`;


export const UpdateUsername = gql`
    mutation UpdateAccount(
        $uid: uuid!,
        $username: String!
      ) {
      update_accounts(
        where: { uid: { _eq: $uid } }
        _set: {
            username: $username
        }
      ) {
        affected_rows
        returning {
          uid
          fullname
          email
          title
          bio
        }
      }
    }
`;

export const IncrementBlockRowIdx = gql`
    mutation IncrementBlockRowIdx(
        $owner_uid: uuid!,
        $page_row_idx: Int!
      ) {
      update_blocks(
        where: {
            owner_uid: { _eq: $owner_uid },
            page_row_idx: { _gte: $page_row_idx }
        }
        _inc: {
            page_row_idx: 1
        }
      ) {
        affected_rows
        returning {
          uid
          page_row_idx
        }
      }
    }
`;

export const SetBlockRowIdx = gql`
    mutation SetBlockRowIdx(
        $uid: uuid!,
        $page_row_idx: Int!
      ) {
      update_blocks_by_pk(
        pk_columns: {uid: $uid}
        _set: {
            page_row_idx: $page_row_idx
        }
      ) {
        page_row_idx
      }
    }
`;

export const EditBlockText = gql`
    mutation EditBlockText(
        $uid: uuid!,
        $text: String!
      ) {
      update_blocks_by_pk(
        pk_columns: {uid: $uid}
        _set: {
            text: $text
        }
      ) {
        page_row_idx
      }
    }
`;

export const InsertBlock = gql`
    mutation InsertBlock($owner_uid: uuid!, $type: Int!, $page_row_idx: Int!) {
      insert_blocks_one(
        object: { owner_uid: $owner_uid, type: $type, page_row_idx: $page_row_idx }
      ) {
        text
      }
    }
`;
