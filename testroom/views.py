from django.shortcuts import render, redirect
from .models import *
# importing Statistics module 
import statistics 
# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_test(my_ip):
	try:
		test = Test.objects.filter(is_finished=False).get(user_ip=my_ip)		
	except Test.DoesNotExist:
		test = None
	
	if not test:
		test = Test.objects.create(user_ip=my_ip)

	return test

def get_sequence():
	result = []
	item = 1
	row_start = 1
	for s in range(1,4):
	    row_start = item
	    for r in range(row_start, row_start+11):
	        item = r
	        for c in range(1,13):
	            result.append(item)
	            #print(item, end=',')
	            item += 11
	        #print('')
	    item = item - 10
	return result

def get_last_test_item_id(test_id):
	result = 0
	test_item_sequence_index_list = []
	sequence = get_sequence()
	try:
		current_test_item_list = TestItem.objects.filter(test_id=test_id)
		if not current_test_item_list:
			return 0
		for ti in current_test_item_list:
			test_item_sequence_index_list.append(sequence.index(ti.item_id.item_id))
		last_test_item_sequence_index = max(test_item_sequence_index_list)
		result = sequence[last_test_item_sequence_index]
	except TestItem.DoesNotExist:
		return 0
	return result

def get_next_item_id(current_id):
    sequence = get_sequence()
    return sequence[sequence.index(current_id)+1]


def index(request):
	my_ip = get_client_ip(request)
	current_test = get_test(my_ip)
	next_item_id = 1
	#sequence = 1
	#submit_button_flag = False
	if request.method == 'POST':
		## Old code
		# print('sequence:' + request.POST['sequence'])
		# sequence = int(request.POST['sequence'])		
		# for idx in range(1,37):
		# 	print('select_item:' + str(idx) + " ==  " + request.POST['select_item_'+str(idx)])
		# 	item_id = int(range(sequence, 397, 11)[idx-1])
		# 	print (item_id)
		# 	obj, created = TestItem.objects.get_or_create(
		# 		test_id=current_test, 
		# 		item_id=Item.objects.get(item_id=item_id), 
		# 		choice_id=ItemChoice.objects.get(choice_id=request.POST['select_item_'+str(idx)]))
		# 	if not created:
		# 		print ("Test Item is already there")
		item_id = int(request.POST['item_id'])
		choice_id = int(request.POST['item_choice'])
		print("test_id: {test}      item_id: {item_id}     choice_id: {choice_id}".format(test=current_test.test_id, item_id=item_id,choice_id=choice_id))
		obj, created = TestItem.objects.get_or_create(
			test_id=current_test, 
			item_id=Item.objects.get(item_id=item_id),
			choice_id=ItemChoice.objects.get(pk=choice_id))
		if not created:
			print ("Error: Test Item is duplicated")
			raise

	
	last_test_item_id = get_last_test_item_id(current_test.test_id)	
	if last_test_item_id:
		print (last_test_item_id)
		if last_test_item_id == 396:
			return redirect('/test/result')
		else:
			next_item_id = get_next_item_id(int(last_test_item_id))
	
	next_item = Item.objects.get(pk=next_item_id)
	subscale_list = Subscale.objects.all()
	
	#data_list = zip(subscale_list, current_sequence)
	#return render(request, 'testroom.html', {'data_list':data_list, 'sequence':sequence, 'submit':submit_button_flag})
	return render(request, 'testroom.html', {'item':next_item})


def calc_test_result(test):
	test_item_list = []
	X = 0
	for test_item in TestItem.objects.filter(test_id=test).order_by('item_id'):
		print("test item id:" + str(test_item.item_id.item_id) + " , choice id:" + str(test_item.choice_id.value))
		test_item_list.append(test_item.choice_id.value)
		X+=test_item.choice_id.value
	M = X/396
	SD = statistics.stdev(test_item_list)
	print("(X:%s - M:%s) / SD:%s" % (X, M, statistics.stdev(test_item_list)))
	return (X-M)/SD, 10, 1

def get_subscales(test):
	index = 1
	sub_index = 1
	test_item_value_list = []
	subscales = {}
	for test_item in TestItem.objects.filter(test_id=test).order_by('item_id'):
		print("test item id:" + str(test_item.item_id.item_id) + " , choice id:" + str(test_item.choice_id.value))
		test_item_value_list.append(test_item.choice_id.value)
		if index == 11:
			subscales[sub_index]=sum(test_item_value_list)
			sub_index += 1
			test_item_value_list=[]
			index = 1
		else:		
			index += 1

	return subscales

def test_result(request):
	my_ip = get_client_ip(request)
	current_test = get_test(my_ip)
	#if not current_test.item_result or not current_test.subscale_result or not current_test.scale_result:
	#item_result, subscale_result, scale_result = calc_test_result(current_test)
	subscales = get_subscales(current_test)
	sorted_subscale_key_list = sorted(subscales, key=subscales.get, reverse=True)
	result = {}
	for s in sorted_subscale_key_list:
		subscale = Subscale.objects.get(pk=s)
		sum_value = subscales[s]
		result[sum_value]=subscale

	return render(request, 'test_result.html', {'sorted_subscales':result})

def save_and_new_test(request):
	my_ip = get_client_ip(request)
	current_test = get_test(my_ip)
	current_test.is_finished = True
	current_test.save()
	return redirect('/')


def admin(request):
	try:
		test_list = Test.objects.all()
	except Test.DoesNotExist:		
		test_list = []
	return render(request, 'test_admin.html', {'test_list':test_list})

def test_detail(request, test_id):
	test_item_list = TestItem.objects.filter(test_id=test_id)
	return render(request, 'test_detail.html', {'test_id':test_id, 'test_item_list':test_item_list})

def test_delete(request, test_id):
	Test.objects.get(pk=test_id).delete()
	return redirect('/test/admin')
