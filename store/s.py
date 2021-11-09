def puzzle(request):
    # 获取选择的单元
    danyuan = request.GET.get('danyuan')
    if ',' in danyuan:
        maxC1 = []
        for dy in danyuan.split(','):
            print(dy, '选择的单元')
            if not dy:
                return render(request, 'puzzle/puzzle.html', {})
            maxC = PuzzleInfo.objects.filter(pdiff=dy)
            print(len(maxC), '套题数量')
            list_maxc = []
            for i in maxC:
                dict1 = model_to_dict(i, exclude=['photot', 'photoa', 'photob', 'photoc', 'photod'])
                dict1['photot'] = ''
                dict1['photoa'] = ''
                dict1['photob'] = ''
                dict1['photoc'] = ''
                dict1['photod'] = ''
                if i.photot.url:
                    dict1['photot'] = i.photot.url
                if i.photoa.url:
                    dict1['photoa'] = i.photoa.url
                if i.photob.url:
                    dict1['photob'] = i.photob.url
                if i.photoc.url:
                    dict1['photoc'] = i.photoc.url
                if i.photod.url:
                    dict1['photod'] = i.photod.url
                # try:
                #     dict1['photot'] = '/media/media' + (i.photot.url.replace('media', ''))
                #     dict1['photoa'] = '/media/media' + (i.photoa.url.replace('media', ''))
                #     dict1['photob'] = '/media/media' + (i.photob.url.replace('media', ''))
                #     dict1['photoc'] = '/media/media' + (i.photoc.url.replace('media', ''))
                #     dict1['photod'] = '/media/media' + (i.photod.url.replace('media', ''))
                # except:
                #     dict1['photot'] = ''
                #     dict1['photoa'] = ''
                #     dict1['photob'] = ''
                #     dict1['photoc'] = ''
                #     dict1['photod'] = ''
                list_maxc.append(dict1)
            maxC = list_maxc
            maxC1 += maxC

        context = {'puzz': maxC1}
        print(context)
        return render(request, 'puzzle/puzzle.html', context)
    else:
        maxC1 = []
        print(danyuan, '选择的单元')
        if not danyuan:
            return render(request, 'puzzle/puzzle.html', {})
        maxC2 = PuzzleInfo.objects.filter(pdiff=danyuan).all()
        print(len(maxC2))
        print("^" * 10)
        print(len(maxC2), '套题数量')
        list_maxc = []
        for i in maxC2:
            # dict1 = model_to_dict(i)
            dict1 = model_to_dict(i, exclude=['photot', 'photoa', 'photob', 'photoc', 'photod'])
            dict1['photot'] = ''
            dict1['photoa'] = ''
            dict1['photob'] = ''
            dict1['photoc'] = ''
            dict1['photod'] = ''
            if i.photot:
                dict1['photot'] = i.photot.url
            if i.photoa:
                dict1['photoa'] = i.photoa.url
            if i.photob:
                dict1['photob'] = i.photob.url
            if i.photoc:
                dict1['photoc'] = i.photoc.url
            if i.photod:
                dict1['photod'] = i.photod.url
            list_maxc.append(dict1)
        maxC2 = list_maxc
        maxC1 += maxC2
        context = {'puzz': maxC1}
        print(context)
        return render(request, 'puzzle/puzzle.html', context)