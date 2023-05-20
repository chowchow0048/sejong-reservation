/*

	API가 완성되기 전 테스트 데이터로 사용하는 내용들입니다.
	내용은 수시로 바뀌나 의미는 없습니다. 개발 완료 후 삭제하도록 합시다.

*/

import getDateStringInThreeDays from '@/assets/scripts/utils/getDateStringInThreeDays.js';
const in3dateStr = getDateStringInThreeDays();

const TESTDATA = {
	// room (회의실)
	rooms_1: [
		{
			id: 0,
			room_name: '835호',
			room_address1: '대양AI센터',
			room_address2: '8층',
			is_usable: 1,
			max_users: 4,
			preview_image: null,
		},
		{
			id: 1,
			room_name: '836호',
			room_address1: '대양AI센터',
			room_address2: '8층',
			is_usable: 1,
			max_users: 4,
			preview_image: null,
		},
	],

	// reservation (예약)
	reservations_min_1: [
		{
			id: 0,
			reservation_type: null,
			reservation_date: in3dateStr.today,
			start_time: '10:00:00',
			end_time: '18:00:00',
			room_id: 0,
			// is_valid: 1,
		},
		{
			id: 1,
			reservation_type: null,
			reservation_date: in3dateStr.tomorrow,
			start_time: '13:00:00',
			end_time: '18:32:00',
			room_id: 1,
			// is_valid: 1,
		},
		{
			id: 2,
			reservation_type: 0,
			reservation_date: in3dateStr.afterTomorrow,
			start_time: '13:00:00',
			end_time: '15:00:00',
			room_id: 1,
			// is_valid: 1,
		},
		{
			id: 3,
			reservation_type: 0,
			reservation_date: '2023-07-30',
			start_time: '13:00:00',
			end_time: '15:00:00',
			room_id: 1,
			// is_valid: 1,
		},
	],
	reservations_max_1: [
		{
			id: 0,
			created_at: '2023-05-17 21:23:42',
			reservation_code: '12345',
			reservation_topic: 'data 1 - single',
			reservation_type: null,
			reservation_date: '2023-05-21',
			start_time: '10:00:00',
			end_time: '18:00:00',
			room_id: 0,
			creator_id: 0,
			members: [
				{ name: 'name1', email: 'mail1' },
				{ name: 'name2', email: 'mail2' },
			],
			is_valid: 1,
			room_used: 0,
		},
		{
			id: 1,
			created_at: '2023-05-17 23:23:42',
			reservation_code: '12345',
			reservation_topic: 'data 2 - single',
			reservation_type: null,
			reservation_date: '2023-05-22',
			start_time: '13:00:00',
			end_time: '18:32:00',
			room_id: 1,
			creator_id: 0,
			members: [
				{ name: 'name22', email: 'mail2' },
				{ name: 'name22', email: 'mail2' },
			],
			is_valid: 1,
			room_used: 0,
		},
		{
			id: 2,
			created_at: '2023-05-16 09:00:00',
			reservation_code: '12345',
			reservation_topic: 'data 3 - multi(0)',
			reservation_type: 0,
			reservation_date: '2023-05-23',
			start_time: '13:00:00',
			end_time: '15:00:00',
			room_id: 1,
			creator_id: 1,
			members: [
				{ name: 'name3', email: 'mail3' },
				{ name: 'name3', email: 'mail3' },
			],
			is_valid: 1,
			room_used: 0,
		},
		{
			id: 3,
			created_at: '2023-05-30 09:00:00',
			reservation_code: '12345',
			reservation_topic: 'data 4 - multi(0)',
			reservation_type: 0,
			reservation_date: '2023-05-30',
			start_time: '13:00:00',
			end_time: '15:00:00',
			room_id: 1,
			creator_id: 1,
			members: [
				{ name: 'name3', email: 'mail3' },
				{ name: 'name3', email: 'mail3' },
			],
			is_valid: 1,
			room_used: 0,
		},
	],
};

export default TESTDATA;
